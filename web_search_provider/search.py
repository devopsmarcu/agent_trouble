from typing import Dict, Any, Type
from .models import SearchOptions, SearchOutput
from .logger import logger
from .exceptions import ProviderNotFoundError, WebSearchError

class SearchFactory:
    _providers: Dict[str, Any] = {}

    @classmethod
    def register_provider(cls, name: str, provider_class: Type):
        cls._providers[name] = provider_class

    @classmethod
    def get_provider(cls, name: str):
        if not cls._providers:
            cls._auto_import_providers()
            
        provider_class = cls._providers.get(name.lower())
        if not provider_class:
            raise ProviderNotFoundError(f"Provider {name} not found or not implemented.")
        
        provider_instance = provider_class()
        if not provider_instance.is_configured:
             raise ProviderNotFoundError(f"Provider {name} is enabled but missing API key.")
        return provider_instance
        
    @classmethod
    def _auto_import_providers(cls):
        from .providers import serper, tavily, exa
        cls.register_provider("serper", serper.SerperProvider)
        cls.register_provider("tavily", tavily.TavilyProvider)
        cls.register_provider("exa", exa.ExaProvider)

def searchWeb(query: str, options: dict = None) -> dict:
    opts = SearchOptions(**(options or {}))
    
    providers_to_try = [opts.provider] if opts.provider else opts.providerOrder
    
    for provider_name in providers_to_try:
        try:
            logger.info(f"Attempting search with provider: {provider_name}")
            provider = SearchFactory.get_provider(provider_name)
            
            result: SearchOutput = provider.search(query, opts)
            
            logger.info(f"Search successful with {provider_name}")
            return result.model_dump()
            
        except ProviderNotFoundError as e:
            logger.warning(f"Skipping {provider_name}: {str(e)}")
            continue
        except WebSearchError as e:
             logger.warning(f"Provider {provider_name} failed: {str(e)}. Fallback initiated.")
             continue
        except Exception as e:
             logger.error(f"Unexpected error with {provider_name}: {str(e)}. Fallback initiated.")
             continue
             
    raise WebSearchError("All configured search providers failed or are missing API keys.")
