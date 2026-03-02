class WebSearchError(Exception):
    pass

class ProviderNotFoundError(WebSearchError):
    pass

class ProviderAuthError(WebSearchError):
    pass

class ProviderRateLimitError(WebSearchError):
    pass

class ProviderTimeoutError(WebSearchError):
    pass

class ProviderServerError(WebSearchError):
    pass
