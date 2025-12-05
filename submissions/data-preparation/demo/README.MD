Demo Execution Guide

Setup


Import Code: Create a new Notebook in the workspace and copy the content of src/main.ipynb into it.

Execution

Run the notebook cells in order. The script performs the following steps:

Ingest: Reads Amazon reviews from /databricks-datasets/amazon/test4K.

Clean: Filters empty reviews and imputes missing prices.

Transform: Encodes categories and scales numerical features.

Embed: Downloads a BERT model to generate vector embeddings for reviews.

Store: Saves the result to a Delta table amazon_features.

Note: The embedding generation step runs on the driver node to ensure compatibility with standard/free tier clusters.