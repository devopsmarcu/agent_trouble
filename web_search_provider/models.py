from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field

class SearchOptions(BaseModel):
    maxResults: int = 10
    language: str = "pt"
    country: str = "br"
    timeRange: Optional[Literal["day", "week", "month", "year"]] = None
    safeSearch: bool = True
    includeAnswer: bool = False
    timeoutMs: int = 15000
    providerOrder: List[str] = Field(default_factory=lambda: ["tavily", "serper", "exa"])
    provider: Optional[Literal["tavily", "serper", "exa"]] = None

class SearchResultItem(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None
    publishedAt: Optional[str] = None
    source: Optional[str] = None

class SearchOutput(BaseModel):
    provider: Literal["tavily", "serper", "exa"]
    query: str
    results: List[SearchResultItem]
    answer: Optional[str] = None
    raw: Dict[str, Any]
