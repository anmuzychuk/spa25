import os
import pandas as pd
from pyspark import pipelines as dp
from utilities.utils import process_column
from utilities.constants import VOLUME_PATH

rural_population_csv_filename = "rural_population_percent.csv"
electricity_access_csv_filename = "electricity_access_percent.csv"
gdp_csv_filename = "gdp_data.csv"
mystery_csv_filename = "mystery.csv"

rural_population_path_csv = os.path.join(VOLUME_PATH, rural_population_csv_filename)
electricity_access_path_csv = os.path.join(VOLUME_PATH, electricity_access_csv_filename)
gdp_path_csv = os.path.join(VOLUME_PATH, gdp_csv_filename)
mystery_path_csv = os.path.join(VOLUME_PATH, mystery_csv_filename)

@dp.table(name="bronze.rural_population_csv")
def bronze_projects():
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("skipRows", 4)
        .load(rural_population_path_csv)
    )
    for col in df.columns: 
        clean_col = process_column(col)
        if clean_col != col:
            df = df.withColumnRenamed(col, clean_col)
    return df

@dp.table(name="bronze.electricity_access_csv")
def bronze_projects():
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("skipRows", 4)
        .load(electricity_access_path_csv)
    )
    for col in df.columns: 
        clean_col = process_column(col)
        if clean_col != col:
            df = df.withColumnRenamed(col, clean_col)
    return df

@dp.table(name="bronze.gdp_csv")
def bronze_projects():
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("skipRows", 4)
        .load(gdp_path_csv)
    )
    for col in df.columns: 
        clean_col = process_column(col)
        if clean_col != col:
            df = df.withColumnRenamed(col, clean_col)
    return df

@dp.table(name="bronze.mystery_csv")
def bronze_projects():
    df = (
        spark.read.format("csv")
        .option("header", "true")
        .option("skipRows", 4)
        .load(mystery_path_csv)
    )
    for col in df.columns: 
        clean_col = process_column(col)
        if clean_col != col:
            df = df.withColumnRenamed(col, clean_col)
    return df