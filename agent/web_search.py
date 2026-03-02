from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from web_search_provider.search import searchWeb
import json

llm = Ollama(model="mistral", request_timeout=360.0)

def search_web(query_str: str) -> dict:
    fallback_prompt = f"Por favor, ajude com o seguinte problema de suporte técnico: {query_str}. RESPONDA MANTENDO O IDIOMA PORTUGUÊS DO BRASIL. Não responda em inglês."
    
    try:
        options = {
            "maxResults": 3,
            "includeAnswer": True,
            "providerOrder": ["tavily", "serper", "exa"],
            "timeoutMs": 15000
        }
        res = searchWeb(query_str, options)
        results = res.get("results", [])
    except Exception as e:
        print(f"Search Web Error: {e}")
        results = []
        
    if not results:
        response = llm.complete(fallback_prompt)
        return {
            "answer": str(response),
            "context": "Pesquisa Web falhou caindo para fallback via LLM base.",
            "url": "N/A"
        }
    
    context_parts = []
    urls_list = []
    
    for r in results:
        url = r.get("url", "N/A")
        snippet = r.get("snippet", "")
        # Adiciona ao contexto apenas se houver algum conteúdo
        if snippet:
            context_parts.append(f"Fonte: {url}\nConteúdo: {snippet}")
        if url != "N/A" and url not in urls_list:
            urls_list.append(url)
            
    context = "\n".join(context_parts)
    urls = ", ".join(urls_list)
    
    # Se o provedor nos mandar a resposta pronta mastigada nativa do motor dele (ex: Answer Box Google), aproveitamos a base
    answer_base = ""
    if res.get("answer"):
         answer_base = f"RESPOSTA RÁPIDA DO MOTOR DE BUSCA:\n{res['answer']}\n\n"
    
    prompt = f"""Use os seguintes trechos de pesquisa web para responder a pergunta de suporte técnico.
    Analise os passos e formule uma solução resolutiva e técnica.
    MUITO IMPORTANTE: Sua resposta final DEVE ESTAR EM PORTUGUÊS DO BRASIL.

    Pergunta/Problema: {query_str}

    {answer_base}
    
    Contextos Web encontrados:
    {context}

    Resposta Detalhada em Português:"""
    
    response = llm.complete(prompt)
    
    return {
        "answer": str(response),
        "context": context,
        "url": urls
    }
