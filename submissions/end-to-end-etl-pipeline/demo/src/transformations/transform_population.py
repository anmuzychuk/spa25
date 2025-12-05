from pyspark import pipelines as dp
from pyspark.sql.functions import coalesce, col, expr
from pyspark.sql.window import Window

@dp.table(name="silver.population")
def merge_population():
    # Merge dfs
    df_csv = spark.read.table("bronze.population_csv").alias("csv")
    df_json = spark.read.table("bronze.population_json").alias("json")

    join_keys = ["CountryCode", "IndicatorCode"]
    all_columns = set(df_csv.columns) | set(df_json.columns)
    non_key_columns = [c for c in all_columns if c not in join_keys]

    df_joined = df_csv.join(
        df_json,
        on=join_keys,
        how="full"
    )

    select_exprs = [col(f"csv.{k}").alias(k) for k in join_keys]
    for c in non_key_columns:
        col_csv = col(f"csv.{c}") if c in df_csv.columns else None
        col_json = col(f"json.{c}") if c in df_json.columns else None
        if col_csv is not None and col_json is not None:
            select_exprs.append(coalesce(col_csv, col_json).alias(c))
        elif col_csv is not None:
            select_exprs.append(col_csv.alias(c))
        elif col_json is not None:
            select_exprs.append(col_json.alias(c))

    merged_df = df_joined.select(select_exprs)
    merged_df = merged_df.filter(col("CountryName") != "Not classified")
    merged_df = merged_df.drop('IndicatorName', 'IndicatorCode')

    # Melt merged_df
    df_melt = merged_df.selectExpr(
        "CountryName",
        "CountryCode",
        "stack(62, " +
        ",".join([f"'{year}', `{year}`" for year in merged_df.columns if year not in ['CountryName', 'CountryCode']]) +
        ") as (year, population)"
    )

    window_spec = (
        Window.partitionBy("CountryName", "CountryCode").orderBy("year")
    )
    df_melt = df_melt.withColumn(
        "population",
        coalesce(
            col("population"),
            expr("last(population, true) over (partition by `CountryName`, `CountryCode` order by year rows between unbounded preceding and current row)"),
            expr("first(population, true) over (partition by `CountryName`, `CountryCode` order by year rows between current row and unbounded following)")
        )
    )

    df_melt = df_melt.filter(col("year").isNotNull())
    df_melt = df_melt.withColumn("population", col("population").cast("int"))
    return df_melt