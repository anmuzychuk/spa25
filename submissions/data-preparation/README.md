Data Preparation

Topic: Data Preparation for Machine Learning in Databricks

Author: Mariis Sirska

Course: Big Data Course

Project Overview

This project demonstrates an end-to-end data preparation pipeline for Machine Learning using Databrick. It shows how to prepare raw, unstructured data (Amazon Reviews) for a sentiment analysis or recommendation model.

The pipeline implements the Medallion Architecture ($Raw \rightarrow Bronze \rightarrow Silver \rightarrow Gold$) and simulates a Feature Store workflow on the free tier of Databricks.

Key Features

Ingestion: Loading parquet data from Databricks public datasets (/databricks-datasets/amazon/test4K).

Cleaning & Imputation: handling missing numerical values (price) using Mean imputation.

Deduplication of text records.

Feature Engineering:

Categorical: One-Hot Encoding for product categories.

Numerical: Standardization (Scaling) of price data.

NLP: Generating Text Embeddings using sentence-transformers for review content.

Feature Store: Simulating a Feature Store by registering the final "Gold" dataset as a Delta Table.

📂 Project Structure

data-preparation-databricks/
├── README.md
├── presentation/
│   └── slides.pdf
├── demo/
│   ├── src/
│   │   └── main.ipynb
│   ├── requirements.txt
│   └── README.md
└── documentation/


How to Run the Demo

Prerequisites

A Databricks account or any Spark environment.

Installation & Setup

Import the Code:

Log in to Databricks.

Create a new Notebook.

Copy the contents of demo/src/main.py into the notebook cells.

Install Dependencies:

The first cell of the script installs the required NLP library:

%pip install sentence-transformers


Run the Pipeline:

Execute the cells sequentially.

The pipeline will ingest data, clean it, generate embeddings, and save the features to a Delta table named amazon_features.

Data Privacy & Security

Data Source: This project uses the public Databricks dataset databricks-datasets/amazon/test4K.

PII: The dataset contains public reviews and does not contain Personally Identifiable Information (PII).

Synthetic Data: Additional columns (Price, Category) are generated synthetically within the script for demonstration purposes.

Secrets: No API keys or passwords are used or stored in this repository.

Technologies Used

Apache Spark (PySpark): Core data processing engine.

Delta Lake: Storage layer for the simulated Feature Store.

Sentence-Transformers: For generating NLP embeddings.

Databricks: Platform for execution.

License

This submission is licensed under the MIT License.