# Databricks notebook source
# MAGIC %pip install -U -q databricks-vectorsearch databricks-langchain mlflow langchain
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import time
from databricks.vector_search.client import VectorSearchClient
from databricks_langchain import DatabricksVectorSearch, ChatDatabricks
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

CATALOG = "main" 
SCHEMA = "default" 
SOURCE_TABLE = f"{CATALOG}.{SCHEMA}.rag_source_docs"
INDEX_NAME = f"{CATALOG}.{SCHEMA}.rag_demo_index"
ENDPOINT_NAME = "vector_search_demo_endpoint"
LLM_MODEL_NAME = "databricks-meta-llama-3-3-70b-instruct"

# COMMAND ----------

sample_docs = [
    {"id": 1, "text": "The Big Data course final project is worth 40% of the grade.", "source": "syllabus"},
    {"id": 2, "text": "Consultations with pan Andrii Muzychuk are held on Tuesdays via Teams.", "source": "syllabus"},
    {"id": 3, "text": "The course covers PySpark, Lakehouse Architecture, and Mosaic AI.", "source": "syllabus"},
]

spark.createDataFrame(sample_docs).write \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(SOURCE_TABLE)

spark.sql(f"ALTER TABLE {SOURCE_TABLE} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
print(f"Source table updated successfully: {SOURCE_TABLE}")

# COMMAND ----------

vsc = VectorSearchClient()
print(f"Triggering sync for index '{INDEX_NAME}'...")

try:
    idx = vsc.get_index(endpoint_name=ENDPOINT_NAME, index_name=INDEX_NAME)
    idx.sync()
    
    while True:
        status = idx.describe().get('status', {})
        if status.get('ready', False):
            print("Index is SYNCED and READY.")
            break
        print(f"Syncing... {status.get('message', 'Processing')}")
        time.sleep(5)

except Exception as e:
    if "not found" in str(e).lower():
        print(f"Index not found. Please run the creation script first.")
    else:
        raise e

# COMMAND ----------

vector_store = DatabricksVectorSearch(
    index_name=INDEX_NAME,
    columns=["id", "text"]
    
)
retriever = vector_store.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
llm = ChatDatabricks(endpoint=LLM_MODEL_NAME)

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# COMMAND ----------

print(f"Running RAG Chain with model: {LLM_MODEL_NAME}...")
result = rag_chain.invoke("What is the weather like today?")
print(f"\nRAG Answer: {result}")

# COMMAND ----------

# MAGIC %md
# MAGIC