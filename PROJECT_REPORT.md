# 📑 Comprehensive Project Report: Customer Churn Prediction Analysis

## Executive Summary
This report documents the end-to-end engineering, machine learning modeling, database persistence, automated QA testing, and business intelligence reporting for the **Customer Churn Prediction Analysis Project (ChurnGuard Enterprise)**.

---

## 1. Introduction
Customer attrition (churn) is a fundamental commercial threat for subscription service businesses. Predicting which customers are likely to cancel their subscriptions allows businesses to proactively execute retention strategies.

---

## 2. Business Problem & Impact
Acquiring new subscribers is **5x to 25x more expensive** than retaining existing accounts. In the telecom sector, average annual churn ranges between 15% and 30%. Predicting churn before it occurs shifts the business model from reactive win-back campaigns to proactive retention alerts.

---

## 3. Dataset Description
We used the IBM Telco Customer Churn dataset comprising **7,043 customer records** and **21 raw feature columns**:
* **Demographics**: `gender`, `SeniorCitizen`, `Partner`, `Dependents`
* **Subscribed Services**: `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`
* **Account Info**: `tenure`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`
* **Target Variable**: `Churn` (`Yes` / `No`)

---

## 4. Data Cleaning & Validation
* Identified 11 blank space strings in `TotalCharges` corresponding to `tenure=0` customers. Replaced blank spaces with `0.0` and cast `TotalCharges` to `float64`.
* Verified zero duplicate customer records (`0` duplicate rows).
* Normalized string column whitespaces and verified data types.

---

## 5. Exploratory Data Analysis (EDA) Highlights
* **Contract Risk**: Month-to-Month contract customers exhibit a **42.7% churn rate**, compared to **11.3%** for 1-Year contracts and **2.8%** for 2-Year contracts.
* **Tenure Impact**: Customers in their first 12 months churn at **47.4%**, whereas tenure $> 60$ months drops churn to **6.6%**.
* **Internet Service**: Fiber Optic subscribers exhibit a **41.9% churn rate**, driven by higher monthly charges ($>\$80.00$).

---

## 6. Feature Engineering & Preprocessing
* Created derived features:
  - `TenureGroup`: Binned tenure into 5 discrete ranges (`0-12Mo`, `12-24Mo`, `24-48Mo`, `48-60Mo`, `60+Mo`).
  - `ChargesPerTenure`: Ratio of total charges to tenure months.
  - `HasAddons`: Count of security/protection add-on services ($0 \to 4$).
* Scaled numerical variables using `StandardScaler` and encoded categorical variables using `OneHotEncoder` via `ColumnTransformer`.

---

## 7. Machine Learning Modeling & Comparison
Trained 5 classification algorithms using stratified 80/20 train-test splits (5,634 train rows, 1,409 test rows):
1. **Logistic Regression**
2. **Decision Tree**
3. **Random Forest**
4. **Gradient Boosting Classifier (Champion)**
5. **XGBoost Classifier**

---

## 8. Model Evaluation & Champion Selection
Evaluated using Accuracy, Precision, Recall, F1-Score, and ROC-AUC:

| Model | Accuracy | F1 Score | **ROC-AUC** |
| :--- | :---: | :---: | :---: |
| **Gradient Boosting** | **`80.48%`** | **`0.5914`** | **`0.8438`** |
| **Logistic Regression** | `80.27%` | `0.5863` | `0.8460` |
| **Decision Tree** | `78.85%` | `0.5669` | `0.8292` |
| **XGBoost** | `77.64%` | `0.5401` | `0.8201` |
| **Random Forest** | `78.00%` | `0.5387` | `0.8177` |

Champion selected: **Gradient Boosting Classifier** due to optimal trade-off between ROC-AUC ($0.8438$) and F1 Score ($0.5914$).

---

## 9. Prediction Pipeline
Built `CustomData` dataclass and `PredictPipeline` inference wrapper supporting 3-tier risk stratification:
* **Low Risk**: Churn Probability $< 30\%$
* **Medium Risk**: Churn Probability $30\% \le P < 65\%$
* **High Risk**: Churn Probability $\ge 65\%$

---

## 10. Streamlit Web Application
Built a 5-page Streamlit application (`app.py`):
1. **Home**: KPI overview & project summary.
2. **Single Customer Prediction**: Form input with Plotly gauge chart and personalized strategy recommendations.
3. **Analytics Dashboard**: Distribution charts and key risk counts.
4. **Prediction History**: Relational database query log table with CSV export.
5. **About Project**: System architecture and model benchmarks.

---

## 11. Relational Database Persistence (MySQL / SQLite)
Integrated SQLAlchemy ORM engine (`src/db/`):
* Normalized tables: `customers`, `predictions`, `model_info`, `application_logs`.
* Automatic SQLite fallback engine ensures local zero-config operation.

---

## 12. Power BI Dashboard Integration
Engineered 5-page Power BI dashboard (`powerbi/`):
* DAX measures for Churn Rate, Retention Rate, Revenue at Risk, and High-Risk Count.
* Interactive slicers for Contract, Payment Method, and Date Range.

---

## 13. Testing & Quality Assurance
Automated 100% test coverage using Pytest (`tests/`):
* **10 Passed, 0 Failed** across Preprocessing, Model, Pipeline, Database CRUD, and Streamlit compilation tests.
* Average inference latency: **`84.75 ms`**.

---

## 14. Deployment Strategy
Prepared zero-downtime deployment pipelines for **Streamlit Community Cloud** and **Render** PaaS platforms.

---

## 15. Key Results Summary
* Champion Model Accuracy: **80.48%**
* ROC-AUC: **0.8438**
* Average Inference Latency: **84.75 ms**
* Automated Unit Test Pass Rate: **100%**

---

## 16. Business Recommendations
1. **Contract Migration**: Target Month-to-Month subscribers with 15% discount incentives to commit to 1-Year contracts.
2. **Onboarding Support**: Provide free TechSupport add-ons during the first 6 months to reduce early tenure churn.
3. **Payment Automation**: Offer a $5 bill credit for switching from Electronic Check to Automatic Bank Transfer.

---

## 17. Future Improvements
* Integrate FastAPI REST endpoints (`/predict`, `/health`).
* Set up automated Slack & Email webhooks for High-Risk account alerts.
* Implement SHAP (SHapley Additive exPlanations) for local feature explanations.

---

## 18. Conclusion
The **ChurnGuard Enterprise** application provides a complete, scalable, end-to-end solution bridging data engineering, machine learning modeling, relational persistence, and interactive executive reporting.
