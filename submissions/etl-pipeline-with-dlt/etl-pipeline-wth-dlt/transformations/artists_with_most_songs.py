# transformations/top_artists_overall.py
from pyspark import pipelines as dp
from pyspark.sql.functions import col, desc, count

@dp.materialized_view(comment="Artists with the highest total number of songs overall.")
def top_artists_overall():
    return (spark.read.table("songs_prepared_validated")
        .groupBy("artist_name")
        .agg(count("*").alias("total_songs"))
        .orderBy(desc("total_songs"))
    )
