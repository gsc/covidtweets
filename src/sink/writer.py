from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import collect_list, current_timestamp, lit
from pyspark.sql.streaming import DataStreamWriter

from src.models.sink_config import SinkConfig
from src.scraper import Scraper, ScraperError


class Writer:
    def __init__(self, sink_config: SinkConfig, scraper: Scraper, spark_logger):
        self.database = sink_config.database
        self.collection = sink_config.collection
        self.checkpoint_location = sink_config.checkpoint_location
        self.processing_time_seconds = sink_config.processing_time_seconds
        self.scraper = scraper
        self.spark_logger = spark_logger

    def enrich_batch(self, batch_df: DataFrame):
        """
        Processes the batch, aggregating the tweets, retrieving and appending the covid cases
        count and adding the timestamp, writing the resulting struct to Mongo.
        """
        if batch_df.isEmpty():
            return

        df = batch_df.agg(collect_list("value"))
        try:
            covid_cases = self.scraper.get_covid_cases()
        except ScraperError as ex:
            self.spark_logger.info(str(ex))
            covid_cases = None

        df = (
            df.withColumn("total_case_count", lit(covid_cases))
            .withColumnRenamed("collect_list(value)", "content")
            .withColumn("timestamp", current_timestamp())
        )

        df.write.format("mongodb").option("spark.mongodb.database", self.database).option(
            "spark.mongodb.collection", self.collection
        ).option("checkpointLocation", self.checkpoint_location).mode("append").save()

    def process(self, df: DataFrame) -> DataStreamWriter:
        query = (
            df.writeStream.trigger(processingTime=f"{self.processing_time_seconds} seconds")
            .outputMode("append")
            .foreachBatch(lambda batch_df, batch_id: self.enrich_batch(batch_df))
            .start()
        )
        return query
