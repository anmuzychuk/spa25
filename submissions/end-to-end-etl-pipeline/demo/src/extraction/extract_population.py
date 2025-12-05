import os
import pandas as pd
from pyspark import pipelines as dp
from utilities.utils import process_column
from utilities.constants import VOLUME_PATH

population_csv_filename = "population/population_data.csv"
population_json_filename = "population/population_data.json"

population_path_csv = os.path.join(VOLUME_PATH, population_csv_filename)
population_path_json = os.path.join(VOLUME_PATH, population_json_filename)

@dp.table(name="bronze.population_csv")
def bronze_population_csv():
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("skipRows", 4)
        .load(population_path_csv)
    )

    for col in df.columns:
        clean_col = process_column(col)
        if clean_col != col:
            df = df.withColumnRenamed(col, clean_col)
    return df

@dp.table(name="bronze.population_json")
def bronze_population_json():
    df = (
        spark.read.format("json")
        .option("header", "true")
        .load(population_path_json)
    )

    for col in df.columns:
        clean_col = process_column(col)
        if clean_col != col:
            df = df.withColumnRenamed(col, clean_col)
    return df