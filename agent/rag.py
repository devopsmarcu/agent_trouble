import os
import unicodedata
from llama_index.core import VectorStoreIndex, StorageContext, Settings, load_index_from_storage
from llama_index.core.prompts import PromptTemplate
from llama_index.core.schema import NodeWithScore, TextNode
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Paths
persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "simple_db")
os.makedirs(persist_dir, exist_ok=True)

# LlamaIndex Settings
SYSTEM_PROMPT = (
    "Você é um assistente técnico especializado em suporte de TI do Hospital Santa Izabel (HSI). "
    "SEMPRE responda em Português do Brasil. "
    "Seja direto, técnico e objetivo."
)
Settings.llm = Ollama(model="mistral", request_timeout=360.0, system_prompt=SYSTEM_PROMPT)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# Prompt que força uso exclusivo do contexto recuperado
QA_PROMPT_TMPL = (
    "Você é um assistente de suporte técnico do HSI. Responda SEMPRE em Português do Brasil.\n"
    "Use EXCLUSIVAMENTE as informações do contexto abaixo para responder a pergunta.\n"
    "Se o contexto não contiver informações suficientes, diga: "
    "'Não encontrei essa informação na base de conhecimento.'\n"
    "NÃO invente, NÃO use conhecimento externo. Use apenas o contexto fornecido.\n\n"
    "Contexto:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n\n"
    "Pergunta: {query_str}\n\n"
    "Resposta em Português:"
)

# Palavras genéricas que não servem como keywords de busca
STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas", "para", "por", "com", "que", "se",
    "me", "te", "lhe", "nos", "vos", "ao", "as", "e", "ou", "mas",
    "eu", "tu", "ele", "ela", "nos", "vos", "eles", "elas",
    "voce", "você", "seu", "sua", "seus", "suas",
    "este", "esta", "esse", "essa", "isso", "isto",
    "qual", "quem", "como", "onde", "quando", "por", "que",
    "sabe", "sobre", "tem", "há", "ser", "ter", "estar",
    "mais", "menos", "muito", "pouco", "bem", "mal", "faz", "fazer",
}


class LocalResponse:
    def __init__(self, text: str, context: str, is_sufficient: bool):
        self.text = text
        self.context = context
        self.is_sufficient = is_sufficient


def normalize_text(s: str) -> str:
    """Remove acentos e coloca em minúsculo para comparação."""
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii").lower()


def extract_keywords(query_str: str) -> list[str]:
    """Extrai palavras-chave normalizadas da query (nomes, termos técnicos, etc.)."""
    words = query_str.replace("?", "").replace("!", "").replace(",", "").split()
    keywords = []
    for word in words:
        w_norm = normalize_text(word)
        if len(w_norm) >= 4 and w_norm not in STOPWORDS:
            keywords.append(w_norm)
    return keywords


def get_index():
    try:
        if os.path.exists(os.path.join(persist_dir, "docstore.json")):
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            index = load_index_from_storage(storage_context)
            return index
    except Exception as e:
        print(f"Index error: {e}")
    return None


def keyword_search_all_docs(index, keywords: list[str], max_results: int = 8) -> list[str]:
    """
    Faz busca por keyword em TODOS os documentos do docstore.
    Retorna os conteúdos dos documentos que contêm pelo menos uma keyword.
    """
    docstore = index.storage_context.docstore
    all_docs = docstore.docs  # dict {node_id: BaseNode}

    matched = []
    for node_id, node in all_docs.items():
        content = node.get_content()
        content_norm = normalize_text(content)
        hits = sum(1 for kw in keywords if kw in content_norm)
        if hits > 0:
            matched.append((hits, content))

    # Ordena por quantidade de keywords encontradas (mais relevante primeiro)
    matched.sort(key=lambda x: x[0], reverse=True)

    print(f"  Keyword search total: {len(matched)} docs encontrados com {keywords}")
    return [content for _, content in matched[:max_results]]


def query_local_db(query_str: str) -> LocalResponse | None:
    index = get_index()
    if not index:
        return LocalResponse("", "", False)

    keywords = extract_keywords(query_str)
    print(f"  Keywords extraídas: {keywords}")

    context_parts = []

    # --- Camada 1: Busca por keyword em TODOS os documentos ---
    if keywords:
        keyword_docs = keyword_search_all_docs(index, keywords, max_results=8)
        context_parts.extend(keyword_docs)
        print(f"  Contexto via keyword: {len(keyword_docs)} docs")

    # --- Camada 2: Busca vetorial (semântica) como complemento ---
    try:
        retriever = index.as_retriever(similarity_top_k=5)
        vector_nodes = retriever.retrieve(query_str)

        # Adiciona nodes vetoriais que não estejam já no contexto por keyword
        existing_content = set(context_parts)
        added_vector = 0
        for node in vector_nodes:
            content = node.get_content()
            if content not in existing_content:
                context_parts.append(content)
                existing_content.add(content)
                added_vector += 1
            if added_vector >= 3:
                break

        print(f"  Contexto via vetor: +{added_vector} docs adicionais")
    except Exception as e:
        print(f"  Vector search error: {e}")

    if not context_parts:
        return LocalResponse("", "", False)

    context_str = "\n\n---\n\n".join(context_parts)

    # Envia para o LLM com o prompt que proíbe invenção
    prompt = QA_PROMPT_TMPL.format(
        context_str=context_str,
        query_str=query_str
    )

    llm = Settings.llm
    response = llm.complete(prompt)
    resp_text = str(response).strip()

    INSUFFICIENT_PHRASES = [
        "não encontrei essa informação",
        "não sei", "não tenho contexto", "not mentioned",
        "não há informações", "vazio",
        "i don't know", "i do not know", "no information",
        "cannot answer", "no context", "not provided",
        "sem informação", "sem contexto", "not found",
        "empty", "no relevant",
    ]

    is_sufficient = (
        bool(context_parts)
        and len(resp_text) > 20
        and not any(phrase in resp_text.lower() for phrase in INSUFFICIENT_PHRASES)
    )

    return LocalResponse(resp_text, context_str, is_sufficient)
