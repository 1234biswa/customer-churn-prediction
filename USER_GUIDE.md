# 📖 User Navigation & Operational Manual

Welcome to the **ChurnGuard Enterprise User Manual**. This guide explains how business managers, customer success agents, and data analysts can navigate and utilize each module of the application.

---

## 🎯 Navigation Overview

The sidebar radio buttons allow seamless navigation across 5 core modules:

```text
📊 ChurnGuard Enterprise
  ├── 🏠 Home
  ├── 🎯 Single Customer Prediction
  ├── 📈 Analytics Dashboard
  ├── 📜 Prediction History
  └── ℹ️ About Project
```

---

## 🏠 Module 1: Home Page
* **Purpose**: Overview of analyzed profiles (`7,043`), model accuracy (`80.48%`), ROC-AUC score (`0.8438`), and business objectives.
* **Usage**: Ideal for getting a quick executive snapshot of platform performance.

---

## 🎯 Module 2: Single Customer Risk Calculator
* **Purpose**: Predict churn risk for individual customer accounts.
* **Operational Steps**:
  1. Fill in customer demographics (`Gender`, `Senior Citizen`, `Partner`, `Dependents`).
  2. Select subscribed services (`Phone`, `Internet Service`, `Online Security`, `Tech Support`, `Streaming`).
  3. Input contract & billing details (`Contract Type`, `Tenure Months`, `Monthly Charges ($)`).
  4. Click **🚀 Generate Churn Risk Score**.
* **Interpreting Results**:
  - **Plotly Gauge Chart**: Displays continuous risk probability ($0\% \to 100\%$).
  - **Risk Badges**:
    - 🟢 **Low Risk (0-30%)**: Stable customer; prime candidate for loyalty rewards.
    - 🟡 **Medium Risk (31-65%)**: Vulnerable customer; recommend bundling TechSupport add-ons.
    - 🔴 **High Risk (66-100%)**: High cancellation risk; immediate intervention required (offer 15% contract renewal discount).

---

## 📈 Module 3: Executive Analytics Dashboard
* **Purpose**: Aggregate analytics on historical prediction trends.
* **Usage**: View total queries, risk distribution pie charts, and churn risk grouped by contract type.

---

## 📜 Module 4: Prediction History & Export
* **Purpose**: Audit database records and export logs.
* **Operational Steps**:
  1. Use the search bar to filter records by `Customer ID` or `Contract Type`.
  2. Click **📥 Export Prediction Logs to CSV** to download the query log for offline spreadsheet analysis.

---

## 📊 Module 5: Power BI Interactive Dashboard
* **Purpose**: Executive reporting across 5 interactive pages.
* **Usage**: Open `powerbi/powerbi_customer_churn_dataset.csv` inside Power BI Desktop to slice by demographics, payment methods, and monthly revenue at risk.
