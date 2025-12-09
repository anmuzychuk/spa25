# transformations/songs_by_year.py
from pyspark import pipelines as dp
from pyspark.sql.functions import col, count

@dp.materialized_view(comment="Counts of songs released per year.")
def songs_by_year():
    return (spark.read.table("songs_prepared_validated")
        .filter(col("year") > 0)
        .groupBy("year")
        .agg(count("*").alias("total_songs"))
        .sort("year")
    )
