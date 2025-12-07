# Mosaic AI Agents & RAG Demo

> A demonstration of building RAG systems and ReAct agents on Databricks using Mosaic AI, LangChain, and Unity Catalog.

## 📁 Project Structure

```
mosaic-agents/
├── README.md           # Project documentation
├── AGENT.py           # ReAct Agent implementation with custom tools
├── RAG.py             # Basic RAG pipeline implementation
├── AGENT.dbc          # Databricks notebook for Agent
├── RAG.dbc            # Databricks notebook for RAG
└── building_agents_in_databricks_with_mosaic_ai.pdf    # Project presentation and documentation
```

## Overview

This project showcases how to leverage Databricks Mosaic AI components to build intelligent applications. It covers two main scenarios:

1.  **Retrieval-Augmented Generation (RAG)**: In `RAG.py`, I demonstrate how to:
    -   Ingest raw text data into a Delta table.
    -   Create and sync a **Databricks Vector Search** index.
    -   Build a LangChain retrieval chain to answer questions based on the indexed documents.

2.  **AI Agents**: In `AGENT.py`, we build a **ReAct Agent** that can:
    -   Use the Vector Search index as a retrieval tool to answer course-related questions.
    -   Execute **Unity Catalog Functions** (e.g., `calculate_final_grade`) to perform specific calculations.
    -   Log the agent to MLflow for deployment and serving.

## Prerequisites

To run this project, you need access to a Databricks Workspace with:
-   **Unity Catalog** enabled.
-   **Serverless Compute** or a cluster running DBR 14.3 LTS ML or higher.
-   A **Vector Search Endpoint** named `vector_search_demo_endpoint` (or update the code to match your endpoint).
-   Access to LLM models via **Databricks Model Serving** (default: `databricks-meta-llama-3-3-70b-instruct`).

## Setup & Usage

1.  **Environment Setup**:
    -   Ensure your Databricks environment is set up with the necessary permissions to create catalogs, schemas, and vector search endpoints.
    -   Install required libraries: `langgraph`, `databricks-langchain`, `mlflow`, `langchain`, `faiss-cpu`.

2.  **Running the RAG Demo**:
    -   Open `RAG.py` (or `RAG.dbc`).
    -   Run the cells to create the source table `main.default.rag_source_docs` and sync the vector index.
    -   Test the retrieval chain with sample queries.

3.  **Running the Agent Demo**:
    -   Open `AGENT.py` (or `AGENT.dbc`).
    -   Run the setup cells to define the `course_info_retriever` tool and the `calculate_final_grade` UC function.
    -   Execute the agent to see it reason and use tools to answer complex queries like "What is my grade if...".
    -   The agent will be logged to MLflow under `main.default.big_data_agent`.

## Information

-   **Author**: Taras Lysun
-   **Course**: Big Data Course @ UCU (2025)

