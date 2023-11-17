from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=False)
class SparkConfig:
    app_name: str
    termination_policy: str
    window_duration: str = "20 seconds"
