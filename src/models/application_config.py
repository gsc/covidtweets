from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.models.base_config import BaseConfig
from src.models.spark_config import SparkConfig


@dataclass(frozen=False)
class ApplicationConfig:
    base_config: BaseConfig
    spark_config: SparkConfig


@dataclass(frozen=False)
class Config:
    config: Dict[str, Dict[str, Any]]

    def set_application_config(self) -> ApplicationConfig:
        base_config: Optional[Dict[str, Any]] = self.config.get("base")
        spark_config: Optional[Dict[str, Any]] = self.config.get("spark")
        if base_config is not None and spark_config is not None:
            return ApplicationConfig(
                base_config=BaseConfig(**base_config), spark_config=SparkConfig(**spark_config)
            )
        else:
            raise ValueError("Could not process application config")
