from pyspark import pipelines as dp
from pyspark.sql.functions import col, expr, coalesce
from pyspark.sql.window import Window

@dp.table(name="silver.gdp")
def processed_gdp():
    df_csv = spark.read.table("bronze.gdp_csv")
    df_csv = df_csv.drop('IndicatorName', 'IndicatorCode')

    df_melt = df_csv.selectExpr(
        "CountryName",
        "CountryCode",
        "stack(62, " +
        ",".join([f"'{year}', `{year}`" for year in df_csv.columns if year not in ['CountryName', 'CountryCode']]) +
        ") as (year, gdp)"
    )

    window_spec = (
        Window.partitionBy("CountryName", "CountryCode").orderBy("year")
    )
    df_melt = df_melt.withColumn(
        "gdp",
        coalesce(
            col("gdp"),
            expr("last(gdp, true) over (partition by `CountryName`, `CountryCode` order by year rows between unbounded preceding and current row)"),
            expr("first(gdp, true) over (partition by `CountryName`, `CountryCode` order by year rows between current row and unbounded following)")
        )
    )

    df_melt = df_melt.filter(col("year").isNotNull())
    df_melt = df_melt.withColumn("gdp", col("gdp").cast("float"))
    return df_melt