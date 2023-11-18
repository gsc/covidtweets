from dataclasses import dataclass
from typing import Any, Dict, Optional

from src.models.base_config import BaseConfig
from src.models.scraper_config import ScraperConfig
from src.models.sink_config import SinkConfig
from src.models.source_config import SourceConfig
from src.models.spark_config import SparkConfig


@dataclass(frozen=False)
class ApplicationConfig:
    base_config: BaseConfig
    scraper_config: ScraperConfig
    sink_config: SinkConfig
    source_config: SourceConfig
    spark_config: SparkConfig


@dataclass(frozen=False)
class Config:
    config: Dict[str, Dict[str, Any]]

    def set_application_config(self) -> ApplicationConfig:
        base_config: Optional[Dict[str, Any]] = self.config.get("base")
        scraper_config: Optional[Dict[str, Any]] = self.config.get("scraper")
        sink_config: Optional[Dict[str, Any]] = self.config.get("sink")
        source_config: Optional[Dict[str, Any]] = self.config.get("source")
        spark_config: Optional[Dict[str, Any]] = self.config.get("spark")

        if (
            base_config is not None
            and scraper_config is not None
            and sink_config is not None
            and source_config is not None
            and spark_config is not None
        ):
            return ApplicationConfig(
                base_config=BaseConfig(**base_config),
                scraper_config=ScraperConfig(**scraper_config),
                sink_config=SinkConfig(**sink_config),
                source_config=SourceConfig(**source_config),
                spark_config=SparkConfig(**spark_config),
            )
        else:
            raise ValueError("Could not process application config")
