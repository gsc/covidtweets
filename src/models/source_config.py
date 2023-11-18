from dataclasses import dataclass


@dataclass(frozen=False)
class SourceConfig:
    server: str
    port: int
    processing_time_seconds: int
