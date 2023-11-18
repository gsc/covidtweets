from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import window

from src.models.source_config import SourceConfig
from src.source.cleanup_tweets import cleanup_tweets


class StreamReader:
    def __init__(self, source_config: SourceConfig, spark_session: SparkSession):
        self.server = source_config.server
        self.port = source_config.port
        self.processing_time_seconds = source_config.processing_time_seconds
        self.spark_session = spark_session

    def load(self) -> DataFrame:
        tweets_df = (
            self.spark_session.readStream.format("socket")
            .option("host", self.server)
            .option("port", self.port)
            .option("includeTimestamp", "true")
            .load()
        )

        cleaned_tweets_df = tweets_df.groupBy(
            window(
                tweets_df.timestamp,
                f"{self.processing_time_seconds} seconds",
            )
        ).applyInPandas(cleanup_tweets, schema="value string, timestamp timestamp")

        return cleaned_tweets_df
