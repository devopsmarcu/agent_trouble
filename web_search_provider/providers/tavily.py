from .base import BaseProvider
from ..config import config
from ..models import SearchOptions, SearchOutput, SearchResultItem
from ..normalizer import normalize_string
import requests

class TavilyProvider(BaseProvider):
    def __init__(self):
        super().__init__(config.TAVILY_API_KEY, "tavily")

    def _make_request(self, query: str, options: SearchOptions) -> requests.Response:
        url = "https://api.tavily.com/search"
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced" if options.timeRange else "basic", # Tavily heuristics
            "include_images": options.includeImages,
            "include_answers": options.includeAnswer,
            "max_results": options.maxResults
        }

        # Tavily doesn't use standard Google tbs flags, so day is mapped as follows
        if options.timeRange == "day":
             payload["topic"] = "news"
             payload["days"] = 1
        elif options.timeRange == "week":
             payload["topic"] = "news" 
             payload["days"] = 7
             
        return self._execute_http("POST", url, headers=headers, json_data=payload, timeout=options.timeoutMs)

    def _parse_response(self, query: str, response: requests.Response, options: SearchOptions) -> SearchOutput:
        data = response.json()
        
        tavily_results = data.get("results", [])
        
        results = []
        for r in tavily_results:
             results.append(SearchResultItem(
                 title=normalize_string(r.get("title", r.get("domain", "Sem Título"))),
                 url=normalize_string(r.get("url")),
                 snippet=normalize_string(r.get("content")),
                 publishedAt=normalize_string(r.get("published_date")),
                 source=None
             ))

        answer = normalize_string(data.get("answer")) if options.includeAnswer else None
        
        return SearchOutput(
            provider=self.name,
            query=query,
            results=results[:options.maxResults],
            answer=answer,
            raw=data
        )
