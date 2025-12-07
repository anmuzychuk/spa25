from pyspark import pipelines as dp
from pyspark.sql.functions import coalesce, col, expr
from pyspark.sql.window import Window

@dp.table(name="bronze.rural_electricity")
def concat_rural_electricity():
    df_electricity = spark.read.table("bronze.electricity_access_csv")
    df_rural = spark.read.table("bronze.rural_population_csv")
    return df_electricity.unionByName(df_rural)