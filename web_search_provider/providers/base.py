import requests
import json
import time
from abc import ABC, abstractmethod
from ..models import SearchOptions, SearchOutput, SearchResultItem
from ..normalizer import deduplicate_results, normalize_string
from ..exceptions import ProviderAuthError, ProviderRateLimitError, ProviderServerError, ProviderTimeoutError, WebSearchError
from ..logger import logger

class BaseProvider(ABC):
    def __init__(self, api_key: str | None, name: str):
        self.api_key = api_key
        self.name = name

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key)

    def search(self, query: str, options: SearchOptions) -> SearchOutput:
        for attempt in range(2):
            try:
                response = self._make_request(query, options)
                return self._parse_response(query, response, options)
            except (ProviderRateLimitError, ProviderServerError, ProviderTimeoutError) as e:
                logger.warning(f"Attempt {attempt + 1} failed for {self.name}: {e}")
                if attempt == 1:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                raise WebSearchError(f"Unexpected error in {self.name}: {e}")

    def _execute_http(self, method: str, url: str, headers: dict = None, params: dict = None, json_data: dict = None, timeout: int = 15) -> requests.Response:
         try:
             res = requests.request(method, url, headers=headers, params=params, json=json_data, timeout=timeout/1000.0)
             
             if res.status_code == 401 or res.status_code == 403:
                  raise ProviderAuthError(f"{self.name} Auth failed: {res.text}")
             elif res.status_code == 429:
                  raise ProviderRateLimitError(f"{self.name} Rate limited: {res.text}")
             elif res.status_code >= 500:
                  raise ProviderServerError(f"{self.name} Server error: {res.status_code}")
             
             res.raise_for_status()
             return res
             
         except requests.exceptions.Timeout:
             raise ProviderTimeoutError(f"Request to {self.name} timed out")
         except requests.exceptions.RequestException as e:
             raise WebSearchError(f"HTTP Error in {self.name}: {e}")


    @abstractmethod
    def _make_request(self, query: str, options: SearchOptions) -> requests.Response:
        pass

    @abstractmethod
    def _parse_response(self, query: str, response: requests.Response, options: SearchOptions) -> SearchOutput:
        pass
