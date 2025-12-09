from pyspark import pipelines as dp
from pyspark.sql.functions import col, countDistinct, avg

@dp.materialized_view(
    comment="GOLD: Aggregated metrics of artists grouped by geographic location."
)
@dp.expect("valid_location", "artist_location is not null")
def artists_by_location():
    df = spark.read.table("songs_prepared_validated")
    
    return (
        df.filter(col("artist_location").isNotNull())
          .groupBy("artist_location")
          .agg(
              countDistinct("artist_id").alias("unique_artists"),
              countDistinct("song_title").alias("total_songs"),
              avg("duration").alias("avg_duration"),
              avg("tempo").alias("avg_tempo"),
              avg("loudness").alias("avg_loudness")
          )
          .orderBy("unique_artists", ascending=False)
    )
