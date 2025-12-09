from pyspark import pipelines as dp

@dp.materialized_view(comment="SILVER: Cleaned and merged Million Song Dataset.")
def songs_prepared():
    df_001 = spark.read.table("songs_raw_001")
    df_002 = spark.read.table("songs_raw_002")

    df = (
        df_001.unionByName(df_002)
            .withColumnRenamed("title", "song_title")
    )

    return df

@dp.materialized_view(comment="SILVER: Validated dataset.")
@dp.expect("valid_artist_name", "artist_name IS NOT NULL")
@dp.expect("valid_title", "song_title IS NOT NULL")
@dp.expect("valid_duration", "duration > 0")
@dp.expect_or_drop("valid_year", "year > 0")
def songs_prepared_validated():
    return (spark.read.table("songs_prepared")
            .filter("duration > 0")
            .filter("song_title IS NOT NULL")
            .filter("artist_name IS NOT NULL")
    )

