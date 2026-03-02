import urllib.parse
from typing import List, Any
from .models import SearchResultItem

def clean_url(url: str) -> str:
    """Removes UTM parameters, fragments and normalizes URL for deduplication."""
    try:
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        cleaned_params = {k: v for k, v in query_params.items() if not k.lower().startswith('utm_')}
        cleaned_query = urllib.parse.urlencode(cleaned_params, doseq=True)
        # Remove fragment by setting it to empty string
        return urllib.parse.urlunparse(parsed_url._replace(query=cleaned_query, fragment='')).lower()
    except Exception:
        return url.lower()

def deduplicate_results(results: List[SearchResultItem]) -> List[SearchResultItem]:
    """Deduplicates search results based on cleaned URLs."""
    seen_urls = set()
    deduped = []
    for item in results:
        cleaned_url = clean_url(item.url)
        if cleaned_url not in seen_urls:
            seen_urls.add(cleaned_url)
            deduped.append(item)
    return deduped

def normalize_string(val: Any) -> str | None:
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None
