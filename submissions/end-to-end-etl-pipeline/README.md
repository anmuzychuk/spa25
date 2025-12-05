# End-to-end ETL pipeline

This project implements a simple ETL pipeline using functionality provided by Databricks. The primary module used is the Pipeline, which enables step-by-step operations on a Delta Lake table by executing code according to an automatically generated dependency graph. This approach allows for easier modification and scaling of existing systems compared to traditional methods, such as creating sequences of jobs and manually managing dependencies and execution order.

## 📁 Project Structure

```
end-to-end-etl-pipeline/
├── README.md
├── images/
├── presentation/
│   └── slides.pdf
├── demo/
│   ├── src/
│   │   ├── explorations/
│   │   │   ├── load_analysis.py
│   │   ├── extraction/
│   │   │   ├── extract_others.py
│   │   │   ├── extract_population.py
│   │   │   └── extract_projects.py
│   │   ├── transformations/
│   │   │   ├── concat_rural_electricity.py
│   │   │   ├── merge_population_gdp.py
│   │   │   ├── merge_projects_population_gdp.py
│   │   │   ├── transform_gdp.py
│   │   │   ├── transform_population.py
│   │   │   └── transform_projects.py
│   │   ├── transformations/
│   │   │   ├── constants.py
│   │   │   └── utils.py
│   ├── data/
│   │   |── electricity_access_percent.csv
│   │   |── gdp_data.csv
│   │   |── mystery.csv
│   │   |── population_data.csv
│   │   |── population_data.json
│   │   |── projects_data.csv
│   │   └── rural_population_percent.csv
└── documentation/
    └── report.md
```

## 📧 Contact
- **Author**: Artur Pelcharskyi
- **Project Repository**: https://github.com/PelArtur/BigData-SelfPickedAssignment
- **Presentation Date**: 03-12-2025
- **Course**: Big data processing technologies

