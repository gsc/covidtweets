import json

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import PandasUDFType, collect_list, lit, pandas_udf, window
from pyspark.sql.types import StringType, StructField, StructType

from src.models.application_config import ApplicationConfig, Config
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
        spark_logger.info("Main")

        lines = (
            spark_session.readStream.format("socket")
            .option("host", application_config.base_config.server)
            .option("port", application_config.base_config.port)
            .option("includeTimestamp", "true")
            .load()
        )

        batch = lines.withWatermark("timestamp", "5 minutes")

        def normalize(df):
            url_regexp = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"

            df.value = df.value.str.replace(url_regexp, "", regex=True)
            df.value = df.value.str.replace("#", "")
            df.value = df.value.str.replace("RT:", "")
            return df

        def enrich_batch(batch_df):

            df = batch_df.agg(collect_list("value"))
            df = df.withColumn("total_case_count", lit(123)).withColumnRenamed(
                "collect_list(value)", "content"
            )

            df.write.format("mongodb").option("spark.mongodb.database", "fruits").option(
                "spark.mongodb.collection", "apples"
            ).option("checkpointLocation", "./checkpoint/").mode("append").save()

        batch = batch.groupBy(window(batch.timestamp, "20 seconds")).applyInPandas(
            normalize, schema="value string, timestamp timestamp"
        )

        query = (
            batch.writeStream.trigger(processingTime="20 seconds")
            .outputMode("append")
            .foreachBatch(lambda batch_df, batch_id: enrich_batch(batch_df))
            .start()
        )
        query.awaitTermination()

    except Exception as exc:
        if spark_logger is not None:
            spark_logger.error(str(exc))
        print(str(exc))


if __name__ == "__main__":
    main()
