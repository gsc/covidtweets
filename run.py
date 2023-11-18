import json

import pandas as pd
from pyspark.sql import SparkSession

from src.models.application_config import ApplicationConfig, Config
from src.scraper import Scraper
from src.sink.writer import Writer
from src.source.stream_reader import StreamReader
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

        stream_reader = StreamReader(application_config.source_config, spark_session)
        cleaned_tweets_df = stream_reader.load()

        scraper = Scraper(application_config.scraper_config, spark_logger)
        writer = Writer(application_config.sink_config, scraper, spark_logger)

        query = writer.process(cleaned_tweets_df)
        query.awaitTermination()

    except Exception as exc:
        if spark_logger is not None:
            spark_logger.error(str(exc))
        print(str(exc))


if __name__ == "__main__":
    main()
