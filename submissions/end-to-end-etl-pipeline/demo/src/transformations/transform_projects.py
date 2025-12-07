from pycountry import countries
from collections import defaultdict
from pyspark import pipelines as dp
from utilities.constants import COUNTRIES_DEFAULT_MAPPING
from pyspark.sql.functions import (
    split, col, udf, regexp_replace, to_timestamp, year, dayofmonth, dayofweek
)
from pyspark.sql.types import StringType


@dp.table(name="silver.projects")
def processed_projects():
    df_projects_csv = spark.read.table("bronze.projects_csv")

    # Cleaning data
    df_projects_csv = df_projects_csv.drop("Unnamed: 56")

    df_projects_csv = df_projects_csv.withColumn(
        "Official-Country-Name",
        split(col("countryname"), ";").getItem(0)
    )

    country_names = [row["Official-Country-Name"] for row in df_projects_csv.select("Official-Country-Name").distinct().collect()]
    project_country_abbrev_dict = defaultdict(str)
    country_not_found = []

    for country in sorted(country_names):
        try:
            project_country_abbrev_dict[country] = countries.lookup(country).alpha_3
        except:
            country_not_found.append(country)

    project_country_abbrev_dict.update(COUNTRIES_DEFAULT_MAPPING)

    def get_country_code(country):
        return project_country_abbrev_dict.get(country, "")

    get_country_code_udf = udf(get_country_code, StringType())

    df_projects_csv = df_projects_csv.withColumn(
        "countrycode",
        get_country_code_udf(col("Official-Country-Name"))
    )

    df_projects_csv = df_projects_csv.withColumn(
        "totalamt",
        regexp_replace(col("totalamt"), ",", "").cast("double")
    )

    # Convert dates to timestamp
    df_projects_csv = (
        df_projects_csv
        .withColumn("boardapprovaldate", to_timestamp("boardapprovaldate"))
        .withColumn("closingdate", to_timestamp("closingdate"))
    )

    # Extract time components
    df_projects_csv = (
        df_projects_csv
        .withColumn("year", year("boardapprovaldate"))
        .withColumn("approvalyear", year("boardapprovaldate"))
        .withColumn("approvalday", dayofmonth("boardapprovaldate"))
        .withColumn("approvalweekday", dayofweek("boardapprovaldate"))
        .withColumn("closingyear", year("closingdate"))
        .withColumn("closingday", dayofmonth("closingdate"))
        .withColumn("closingweekday", dayofweek("closingdate"))
    )

    return df_projects_csv.select("id", "countryname", "countrycode", "totalamt", "year")