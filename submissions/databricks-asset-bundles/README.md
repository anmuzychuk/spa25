# Databricks Asset Bundles Project

## Project Overview
The topic of this assignment is **Databricks Asset Bundles (DABs)**. 
This project demonstrates how to manage data pipelines using "Infrastructure as Code" principles by creating a declarative, versioned package that unifies code (SQL) and infrastructure settings.

By moving away from manual UI-based job creation, this project solves common issues such as configuration drift and lack of version control, ensuring that deployments are repeatable and automated

## Prerequisites & Installation

To run this bundle, you must have the Databricks CLI installed.

1.  **Install Databricks CLI**:
    You should install an appropriate version of Databricks CLI according to your OS. You can do it following the official documentation:
    [Databricks CLI Install Documentation](https://docs.databricks.com/aws/en/dev-tools/cli/install)

    > **Important:** Be careful, your version should be **v0.20x or above** to install and run Databricks Asset Bundles correctly.

2.  **Verify Installation**:
    ```bash
    databricks --version
    ```

## Project Architecture & Constraints

### Free Databricks Limitations
This project is specifically designed to work within the limitations of the **Databricks Free Edition**

* **Compute:** The project utilizes a **Serverless SQL Warehouse**.
* **Constraint:** Job Clusters are not supported in the Free version.
* **Workload:** Consequently, this pipeline runs **SQL tasks** exclusively. Python/PySpark tasks are avoided as they require Job Clusters which cause deployment failures in the free version.

### Workflow Implemented
The development lifecycle follows these standard DAB steps:

1.  **Init:** Initialize the bundle structure.
2.  **Configuration (`databricks.yml`):** Define resources and variables.
3.  **Validate:** `databricks bundle validate` checks the YAML syntax.
4.  **Deploy:** `databricks bundle deploy` uploads files and creates the job in the workspace.
5.  **Run:** `databricks bundle run` executes the defined tasks.

if all is complete successfully you can check results of queries in Databricks
## Project Structure

```text
topic-name/
├── README.md               
├── presentation/
│   └── slides.pdf         
├── demo/                   
│   ├── databricks.yml      
|   ├── data
|   ├── scratch
|   |   └── exploration.ipynb
|   |   └── README.md
│   ├── resources/
│   │   └── test100_sql.job.yml     
│   └── src/
│       └── my_query.sql    
└── documentation/
    └── report.md
```

## How to run

1. navigate to the bundle directory:
```
cd demo
```

2. authenticate (you can do it via a token from Databricks):
```
databricks auth login
```

3. validate configuration:
```
databricks bundle validate
```

4. deploy the bundle
```
databricks bundle deploy
```

5. run the bundle:
```
databricks bundle run sql_executin_job
```