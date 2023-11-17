from dataclasses import dataclass


@dataclass(frozen=False)
class BaseConfig:
    environment: str
    log_level: str
    server: str
    port: int
