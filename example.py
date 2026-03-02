from web_search_provider.search import searchWeb
from web_search_provider.logger import logger
import json

if __name__ == "__main__":
    # Necessário declarar chaves no .env ou terminal:
    # export TAVILY_API_KEY="..."
    # export SERPER_API_KEY="..."
    logger.info("Iniciando teste manual de buscas na Web (com fallback)")
    
    query = "Como consertar erro de Active Directory trust?"
    options = {
        "maxResults": 3,
        "includeAnswer": True,
        # Tavily tentará primeiro. Se falhar / chave nula -> Serper. Se falhar -> Exa.
        "providerOrder": ["tavily", "serper", "exa"], 
        "timeoutMs": 10000
    }
    
    try:
        resultado = searchWeb(query, options)
        print("\n=== BUSCA COMPLETA COM SUCESSO ===")
        print(f"Provedor utilizado após fallback: {resultado['provider']}")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"\nBusca falhou inteiramente: {e}")
