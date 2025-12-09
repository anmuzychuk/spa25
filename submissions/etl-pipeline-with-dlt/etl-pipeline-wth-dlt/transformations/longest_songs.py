# transformations/longest_songs.py
from pyspark import pipelines as dp
from pyspark.sql.functions import col, desc

@dp.materialized_view(comment="Top 10 longest songs per year.")
def longest_songs():
    return (spark.read.table("songs_prepared_validated")
        .filter(col("year") > 0)
        .withColumn("duration_minutes", col("duration") / 60)
        .orderBy(col("year"), desc("duration"))
        .limit(10)
        .select("artist_name", "song_title", "year", "duration_minutes")
    )
