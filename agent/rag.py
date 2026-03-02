import os
from llama_index.core import VectorStoreIndex, StorageContext, Settings, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Paths
persist_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "simple_db")
os.makedirs(persist_dir, exist_ok=True)

# LlamaIndex Settings
Settings.llm = Ollama(model="mistral", request_timeout=360.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

class LocalResponse:
    def __init__(self, text: str, context: str, is_sufficient: bool):
        self.text = text
        self.context = context
        self.is_sufficient = is_sufficient

def get_index():
    try:
        if os.path.exists(os.path.join(persist_dir, "docstore.json")):
            storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
            index = load_index_from_storage(storage_context)
            return index
    except Exception as e:
        print(f"Index error: {e}")
    return None

def query_local_db(query_str: str) -> LocalResponse | None:
    index = get_index()
    if not index:
        return LocalResponse("", "", False)
    
    retriever = index.as_retriever(similarity_top_k=3)
    nodes = retriever.retrieve(query_str)
    
    if not nodes:
        return LocalResponse("", "", False)
    
    query_engine = index.as_query_engine(streaming=False)
    response = query_engine.query(query_str)
    
    resp_text = str(response).strip()
    
    # Avaliação heurística simples para se o local context responde a pergunta
    is_sufficient = bool(nodes) and len(resp_text) > 20 and not any(
        phrase in resp_text.lower() for phrase in [
            "não sei", "não tenho contexto", "not mentioned", "não há informações", "vazio"
        ]
    )
    
    context_str = "\n".join([n.get_content() for n in nodes])
    
    return LocalResponse(resp_text, context_str, is_sufficient)
