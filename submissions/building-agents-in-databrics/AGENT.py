# Databricks notebook source
# MAGIC %pip install -U -q langgraph>=0.2.0 databricks-langchain mlflow langchain faiss-cpu
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

import pandas as pd
import mlflow
import time

from databricks.vector_search.client import VectorSearchClient
from databricks_langchain import ChatDatabricks, DatabricksVectorSearch, UCFunctionToolkit
from langchain_core.tools import tool # <--- The Clean Fix
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

CATALOG = "main"
SCHEMA = "default"
TABLE_NAME = "raw_documentation"
INDEX_NAME = f"{CATALOG}.{SCHEMA}.rag_demo_index"
ENDPOINT_NAME = "vector_search_demo_endpoint"
LLM_MODEL_NAME = "databricks-meta-llama-3-3-70b-instruct"

# COMMAND ----------

data = [
    {"id": 1, "text": "The Big Data course final project is worth 40% of the grade.", "source": "syllabus"},
    {"id": 2, "text": "Consultations with Andrii Muzychuk are held on Tuesdays via Teams.", "source": "syllabus"},
    {"id": 3, "text": "The course covers PySpark, Lakehouse Architecture, and Mosaic AI.", "source": "syllabus"},
]

df = spark.createDataFrame(pd.DataFrame(data))
df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{CATALOG}.{SCHEMA}.{TABLE_NAME}")
spark.sql(f"ALTER TABLE {CATALOG}.{SCHEMA}.{TABLE_NAME} SET TBLPROPERTIES (delta.enableChangeDataFeed = true)")
print("Data updated.")

# COMMAND ----------

vsc = VectorSearchClient()
print(f"Checking index '{INDEX_NAME}'...")
try:
    idx = vsc.get_index(endpoint_name=ENDPOINT_NAME, index_name=INDEX_NAME)
    idx.sync()
    while True:
        status = idx.describe().get('status', {})
        if status.get('ready', False):
            print("Index is SYNCED and READY.")
            break
        time.sleep(2)
except Exception as e:
    print(f"Warning: Ensure index exists. Error: {e}")

# COMMAND ----------

vector_store = DatabricksVectorSearch(
    index_name=INDEX_NAME,
    columns=["id", "text"]
)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

@tool
def course_info_retriever(query: str) -> str:
    """docs"""
    docs = retriever.invoke(query)
    return "\n\n".join([d.page_content for d in docs])

function_name = f"{CATALOG}.{SCHEMA}.calculate_final_grade"
spark.sql(f"""
CREATE OR REPLACE FUNCTION {function_name}(current_points DOUBLE, project_score DOUBLE)
RETURNS DOUBLE
LANGUAGE PYTHON
COMMENT 'Calculates the final course grade.'
AS $$
    return current_points + (project_score * 0.4)
$$
""")
uc_toolkit = UCFunctionToolkit(function_names=[function_name])

all_tools = [course_info_retriever] + uc_toolkit.tools

# COMMAND ----------

llm = ChatDatabricks(endpoint=LLM_MODEL_NAME)

agent_graph = create_react_agent(llm, all_tools)

print(f"Running Agent with model: {LLM_MODEL_NAME}...")

input_message = "I have 45 points so far. If I score 90 on the final project, what is my total grade?"
response = agent_graph.invoke({"messages": [HumanMessage(content=input_message)]})
print("--- Execution Trace ---")
for msg in response['messages']:
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tool in msg.tool_calls:
            print(f"Tool Called: {tool['name']}")
            print(f"   Args: {tool['args']}")
            print(f"   ID:   {tool['id']}")
            print("-" * 20)
print(f"\nFinal Answer: {response['messages'][-1].content}")

# COMMAND ----------

llm = ChatDatabricks(endpoint=LLM_MODEL_NAME)

agent_graph = create_react_agent(llm, all_tools)

print(f"Running LangGraph Agent with model: {LLM_MODEL_NAME}...")

input_message = "Who is conducting consultations?"
response = agent_graph.invoke({"messages": [HumanMessage(content=input_message)]})
for msg in response['messages']:
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tool in msg.tool_calls:
            print(f"Tool Called: {tool['name']}")
            print(f"   Args: {tool['args']}")
            print(f"   ID:   {tool['id']}")
            print("-" * 20)
print(f"\nFinal Answer: {response['messages'][-1].content}")

# COMMAND ----------

mlflow.set_registry_uri("databricks-uc")
model_name = f"{CATALOG}.{SCHEMA}.big_data_agent"

with mlflow.start_run(run_name="uc_agent_run_langgraph") as run:
    model_info = mlflow.langchain.log_model(
        lc_model=agent_graph,
        artifact_path="agent",
        registered_model_name=model_name,
        input_example={"messages": [{"role": "user", "content": "What is the project weight?"}]},
        pip_requirements=[
            "langchain", 
            "langgraph",
            "databricks-langchain", 
            "databricks-vectorsearch", 
            "databricks-agents"
        ]
    )
print(f"Agent logged to: {model_name}")