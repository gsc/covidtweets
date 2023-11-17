from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import collect_list, lit
from pyspark.sql.streaming import DataStreamWriter

from src.models.sink_config import SinkConfig


class Writer:
    def __init__(self, sink_config: SinkConfig):
        self.database = sink_config.database
        self.collection = sink_config.collection
        self.checkpoint_location = sink_config.checkpoint_location
        self.processing_time_seconds = sink_config.processing_time_seconds

    def enrich_batch(self, batch_df):
        df = batch_df.agg(collect_list("value"))
        df = df.withColumn("total_case_count", lit(123)).withColumnRenamed(
            "collect_list(value)", "content"
        )

        # TODO: Add the timestamp
        df.write.format("mongodb").option("spark.mongodb.database", self.database).option(
            "spark.mongodb.collection", self.collection
        ).option("checkpointLocation", self.checkpoint_location).mode("append").save()

    def process(self, df: DataFrame) -> DataStreamWriter:
        # self.spark_logger.info("Processing dataframe ")

        query = (
            df.writeStream.trigger(processingTime=f"{self.processing_time_seconds} seconds")
            .outputMode("append")
            .foreachBatch(lambda batch_df, batch_id: self.enrich_batch(batch_df))
            .start()
        )
        return query
