from .base import BaseProvider
from ..config import config
from ..models import SearchOptions, SearchOutput, SearchResultItem
from ..normalizer import normalize_string
import requests

class SerperProvider(BaseProvider):
    def __init__(self):
        super().__init__(config.SERPER_API_KEY, "serper")

    def _make_request(self, query: str, options: SearchOptions) -> requests.Response:
        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            "q": query,
            "gl": options.country,
            "hl": options.language,
            "num": options.maxResults
        }
        
        # Mapping timeRange for Google/Serper
        if options.timeRange == "day":
             payload["tbs"] = "qdr:d"
        elif options.timeRange == "week":
             payload["tbs"] = "qdr:w"
        elif options.timeRange == "month":
             payload["tbs"] = "qdr:m"
        elif options.timeRange == "year":
             payload["tbs"] = "qdr:y"

        return self._execute_http("POST", url, headers=headers, json_data=payload, timeout=options.timeoutMs)

    def _parse_response(self, query: str, response: requests.Response, options: SearchOptions) -> SearchOutput:
        data = response.json()
        
        organic_results = data.get("organic", [])
        
        results = []
        for r in organic_results:
             results.append(SearchResultItem(
                 title=normalize_string(r.get("title")),
                 url=normalize_string(r.get("link")),
                 snippet=normalize_string(r.get("snippet")),
                 publishedAt=normalize_string(r.get("date")),
                 source=None  # Serper typically doesn't give a separate 'source' from snippet
             ))
             
        answer = None
        if options.includeAnswer and data.get("answerBox"):
             answer = normalize_string(data["answerBox"].get("snippet") or data["answerBox"].get("answer"))

        return SearchOutput(
            provider=self.name,
            query=query,
            results=results[:options.maxResults],
            answer=answer,
            raw=data
        )
