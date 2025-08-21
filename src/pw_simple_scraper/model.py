from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class ScrapeResult:
    """Data class to hold the result of a scrape operation."""
    url: str
    selector: str
    result: List[str]
    count: int = field(init=False)
    fetched_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        self.count = len(self.result)

    def first(self) -> Optional[str]:
        return self.result[0] if self.result else None

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "selector": self.selector,
            "result": self.result,
            "count": self.count,
            "fetched_at": self.fetched_at.isoformat(),
        }
