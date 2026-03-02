from .base import BaseProvider
from ..config import config
from ..models import SearchOptions, SearchOutput, SearchResultItem
from ..normalizer import normalize_string
import requests

class ExaProvider(BaseProvider):
    def __init__(self):
        super().__init__(config.EXA_API_KEY, "exa")

    def _make_request(self, query: str, options: SearchOptions) -> requests.Response:
        url = "https://api.exa.ai/search"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": query,
            "useAutoprompt": True,  # requested explicit option
            "type": "neural",
            "numResults": options.maxResults,
            "contents": {
                "text": True
            }
        }
        
        return self._execute_http("POST", url, headers=headers, json_data=payload, timeout=options.timeoutMs)

    def _parse_response(self, query: str, response: requests.Response, options: SearchOptions) -> SearchOutput:
        data = response.json()
        
        exa_results = data.get("results", [])
        
        results = []
        for r in exa_results:
             results.append(SearchResultItem(
                 title=normalize_string(r.get("title")),
                 url=normalize_string(r.get("url")),
                 snippet=normalize_string(r.get("text")[:500] if r.get("text") else None), # Trim content
                 publishedAt=normalize_string(r.get("publishedDate")),
                 source=normalize_string(r.get("author"))
             ))
             
        return SearchOutput(
            provider=self.name,
            query=query,
            results=results[:options.maxResults],
            answer=None,
            raw=data
        )
