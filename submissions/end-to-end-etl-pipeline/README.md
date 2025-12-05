# End-to-end ETL pipeline

This project implements a simple ETL pipeline using functionality provided by Databricks. The primary module used is the Pipeline, which enables step-by-step operations on a Delta Lake table by executing code according to an automatically generated dependency graph. This approach allows for easier modification and scaling of existing systems compared to traditional methods, such as creating sequences of jobs and manually managing dependencies and execution order.

## 📁 Project Structure

```
end-to-end-etl-pipeline/
├── README.md
├── presentation/
│   └── slides.pdf
├── demo/
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   └── utils.py
│   ├── data/
│   │   └── sample_data.csv
│   ├── requirements.txt
│   └── README.md
└── documentation/
    └── report.md
```

## 📧 Contact
- **Author**: Artur Pelcharskyi
- **Project Repository**: https://github.com/PelArtur/BigData-SelfPickedAssignment
- **Presentation Date**: 03-12-2025
- **Course**: Big data processing technologies

