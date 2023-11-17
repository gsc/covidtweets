from dataclasses import dataclass


@dataclass(frozen=False)
class SinkConfig:
    database: str
    collection: str
    checkpoint_location: str
    processing_time_seconds: int
