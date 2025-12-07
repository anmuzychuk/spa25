from pyspark import pipelines as dp

@dp.table(name="gold.countrydata")
def processed_countrydata():
    df_gdp_population = spark.read.table("silver.population_gdp")
    df_projects = spark.read.table("silver.projects")
    df_projects = df_projects.drop("countryname")

    df_merged = (
        df_projects
        .join(
            df_gdp_population,
            on=["countrycode", "year"],
            how="left"
        )
        .dropna(subset=["population"])
    )
    return df_merged
