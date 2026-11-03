# 📜 Changelog

All notable changes to the **Customer Churn Prediction Analysis (ChurnGuard Enterprise)** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-08-07

### 🚀 Added
- **Data Ingestion & Cleaning**: Ingestion pipeline (`src/components/data_ingestion.py`) and data cleaning module (`src/components/data_cleaning.py`) handling blank `TotalCharges` space replacement.
- **Exploratory Data Analysis (EDA)**: Visual EDA module (`src/components/eda.py`) generating 8 analytical report charts.
- **Feature Engineering & Preprocessing**: `FeatureEngineer` component (`TenureGroup`, `ChargesPerTenure`, `HasAddons`) and `DataPreprocessor` with `ColumnTransformer`.
- **Model Training & Comparison**: Modular trainer (`src/components/model_training.py`) evaluating 5 classifiers (Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, XGBoost).
- **Model Evaluation**: Champion model selection (`src/components/model_evaluation.py`) selecting Gradient Boosting Classifier (Accuracy: 80.48%, ROC-AUC: 0.8438).
- **Prediction Pipeline**: Serialization saver (`src/components/model_saver.py`) and reusable inference pipeline (`src/pipeline/predict_pipeline.py`) with 3-tier risk stratification.
- **Streamlit Web UI**: 5-page enterprise SaaS application (`app.py`) with Plotly gauge visuals and SaaS CSS styling.
- **Relational Persistence**: SQLAlchemy database layer (`src/db/`) supporting MySQL and automatic SQLite fallback.
- **Automated Pytest Suite**: 100% test coverage (`tests/`) verifying preprocessing, model inference, prediction pipeline, database CRUD, and UI compilation.
- **Power BI Dashboard**: 5-page Power BI report specification (`powerbi/`) with DAX measures and automated CSV exporter (`powerbi/powerbi_export_data.py`).
- **Cloud Deployment Prep**: `.streamlit/config.toml`, `runtime.txt`, `DEPLOYMENT_GUIDE.md`, and environment variable configuration for Streamlit Community Cloud and Render.
