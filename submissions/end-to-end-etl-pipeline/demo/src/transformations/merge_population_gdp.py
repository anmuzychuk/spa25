from pyspark import pipelines as dp
from utilities.constants import NON_COUNTRIES

@dp.table(name="silver.population_gdp")
def merge_population_gdp():
    df_gdp = spark.read.table("silver.gdp")
    df_population = spark.read.table("silver.population")

    df = df_gdp.join(df_population, on=['CountryName', 'CountryCode', 'year'])
    df = df.filter(~df['CountryName'].isin(NON_COUNTRIES))
    df = df.withColumnRenamed("CountryName", "countryname").withColumnRenamed("CountryCode", "countrycode")
    return df