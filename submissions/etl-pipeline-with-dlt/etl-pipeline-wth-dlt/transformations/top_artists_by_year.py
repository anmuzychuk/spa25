from pyspark import pipelines as dp
from pyspark.sql.functions import desc, expr

@dp.materialized_view(comment="A table summarizing counts of songs released by the artists who released the most songs each year.")
def top_artists_by_year():
    return (spark.read.table("songs_prepared_validated")
        .filter(expr("year > 0"))
        .groupBy("artist_name", "year")
        .count().withColumnRenamed("count", "total_number_of_songs")
        .sort(desc("total_number_of_songs"), desc("year"))
    )
