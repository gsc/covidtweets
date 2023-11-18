import json

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import PandasUDFType, pandas_udf, window
from pyspark.sql.types import StringType, StructField, StructType

from src.models.application_config import ApplicationConfig, Config
from src.scraper import Scraper
from src.sink.writer import Writer
from src.source.cleanup_tweets import cleanup_tweets
from src.utils.parser import Parser


def main():
    spark_session = None
    spark_logger = None

    try:
        parser = Parser()

        application_config: ApplicationConfig = Config(
            config=parser.read(file=parser.get_args().config_file_name)
        ).set_application_config()

        spark_session = SparkSession.builder.appName(
            application_config.spark_config.app_name
        ).getOrCreate()
        spark_session.sparkContext.setLogLevel(application_config.base_config.log_level)
        log4j = spark_session._jvm.org.apache.log4j
        spark_logger = log4j.LogManager.getLogger(application_config.spark_config.app_name)

        lines = (
            spark_session.readStream.format("socket")
            .option("host", application_config.base_config.server)
            .option("port", application_config.base_config.port)
            .option("includeTimestamp", "true")
            .load()
        )

        batch = lines.withWatermark("timestamp", "5 minutes")

        batch = batch.groupBy(
            window(
                batch.timestamp, f"{application_config.sink_config.processing_time_seconds} seconds"
            )
        ).applyInPandas(cleanup_tweets, schema="value string, timestamp timestamp")
        scraper = Scraper(application_config.scraper_config, spark_logger)
        writer = Writer(application_config.sink_config, scraper, spark_logger)
        query = writer.process(batch)
        query.awaitTermination()

    except Exception as exc:
        if spark_logger is not None:
            spark_logger.error(str(exc))
        print(str(exc))


if __name__ == "__main__":
    main()
