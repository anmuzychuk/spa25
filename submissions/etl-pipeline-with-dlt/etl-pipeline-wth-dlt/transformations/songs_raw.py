from pyspark import pipelines as dp
from schemas import songs_schema


# --- RAW TABLE 1: data-001 ---
file_path_001 = "/databricks-datasets/songs/data-001/"

@dp.table(comment="Raw data from songs data-001 folder.")
def songs_raw_001():
    return (
        spark.readStream
            .format("cloudFiles")
            .schema(songs_schema)
            .option("cloudFiles.format", "csv")
            .option("sep", "\t")
            .load(file_path_001)
    )


# --- RAW TABLE 2: data-002 ---
file_path_002 = "/databricks-datasets/songs/data-002/"

@dp.table(comment="Raw data from songs data-002 folder.")
def songs_raw_002():
    return (
        spark.readStream
            .format("cloudFiles")
            .schema(songs_schema)
            .option("cloudFiles.format", "csv")
            .option("sep", "\t")
            .load(file_path_002)
    )
