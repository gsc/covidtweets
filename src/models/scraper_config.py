from dataclasses import dataclass


@dataclass(frozen=False)
class ScraperConfig:
    url: str
