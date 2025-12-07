# Databricks notebook source
import matplotlib.pyplot as plt

# COMMAND ----------

df_res = spark.read.table("etl_catalog.gold.countrydata")
df = df_res.toPandas()

# COMMAND ----------

# MAGIC %md
# MAGIC # Vietnam

# COMMAND ----------

df_vietnam = df[df["countryname"] == "Vietnam"]

plt.figure(figsize=(8,5))
plt.plot(df_vietnam["year"], df_vietnam["population"])
plt.title("Vietnam Population Over Time")
plt.xlabel("Year")
plt.ylabel("Population")
plt.grid(True)
plt.tight_layout()
plt.show()

# COMMAND ----------

plt.figure(figsize=(8,5))
plt.plot(df_vietnam["year"], df_vietnam["gdp"])
plt.title("Vietnam GDP Over Time")
plt.xlabel("Year")
plt.ylabel("GDP")
plt.grid(True)
plt.tight_layout()
plt.show()

# COMMAND ----------

plt.figure(figsize=(8,5))
plt.plot(df_vietnam["year"], df_vietnam["gdp"] / df_vietnam["population"])
plt.title("Vietnam GDP per person Over Time")
plt.xlabel("Year")
plt.ylabel("GDP per person")
plt.grid(True)
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Myanmar

# COMMAND ----------

df_myanmar = df[df["countryname"] == "Myanmar"]

# COMMAND ----------

plt.figure(figsize=(8,5))
plt.plot(df_myanmar["year"], df_myanmar["population"])
plt.title("Myanmar Population Over Time")
plt.xlabel("Year")
plt.ylabel("Population")
plt.grid(True)
plt.tight_layout()
plt.show()

# COMMAND ----------

plt.figure(figsize=(8,5))
plt.plot(df_myanmar["year"], df_myanmar["gdp"])
plt.title("Myanmar GDP Over Time")
plt.xlabel("Year")
plt.ylabel("GDP")
plt.grid(True)
plt.tight_layout()
plt.show()

# COMMAND ----------

plt.figure(figsize=(8,5))
plt.plot(df_myanmar["year"], df_myanmar["gdp"] / df_myanmar["population"])
plt.title("Myanmar GDP per person Over Time")
plt.xlabel("Year")
plt.ylabel("GDP per person")
plt.grid(True)
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Myanmar vs Vietnam

# COMMAND ----------

plt.plot(df_vietnam["year"], df_vietnam["population"], label="Vietnam")
plt.plot(df_myanmar["year"], df_myanmar["population"], label="Myanmar")
plt.title("Population Comparison: Vietnam vs Myanmar")
plt.xlabel("Year")
plt.ylabel("Population")
plt.grid(True)
plt.xlim(1978)
plt.legend()
plt.tight_layout()
plt.show()

# COMMAND ----------

plt.plot(df_vietnam["year"], df_vietnam["gdp"], label="Vietnam")
plt.plot(df_myanmar["year"], df_myanmar["gdp"], label="Myanmar")
plt.title("GDP Comparison: Vietnam vs Myanmar")
plt.xlabel("Year")
plt.ylabel("GDP")
plt.grid(True)
plt.xlim(1978)
plt.legend()
plt.tight_layout()
plt.show()

# COMMAND ----------

plt.plot(df_vietnam["year"], df_vietnam["gdp"] / df_vietnam["population"], label="Vietnam")
plt.plot(df_myanmar["year"], df_myanmar["gdp"] / df_myanmar["population"], label="Myanmar")
plt.title("Population Comparison: Vietnam vs Myanmar")
plt.xlabel("Year")
plt.ylabel("Population")
plt.grid(True)
plt.xlim(1978)
plt.legend()
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC # Save data

# COMMAND ----------

import os

# COMMAND ----------

Volume_path = "/Volumes/etl_catalog/default/data/results"
df.to_csv(os.path.join(Volume_path, "country_data.csv"), index=False)
df.to_json(os.path.join(Volume_path, "country_data.json"))