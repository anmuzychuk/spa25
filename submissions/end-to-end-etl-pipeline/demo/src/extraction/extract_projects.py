import os
from pyspark import pipelines as dp
from utilities.utils import process_column
from utilities.constants import VOLUME_PATH

project_filename = "projects/projects_data.csv"
project_path = os.path.join(VOLUME_PATH, project_filename)

@dp.table(name="bronze.projects_csv")
def bronze_projects():
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(project_path)
    )
    for col in df.columns: 
        clean_col = process_column(col)
        if clean_col != col:
            df = df.withColumnRenamed(col, clean_col)
    return df
