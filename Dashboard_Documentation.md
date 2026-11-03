# 📊 Power BI Executive Dashboard Documentation: Customer Churn Analytics

This document provides a comprehensive technical blueprint, DAX measure reference, data model specification, and user guide for the **Customer Churn Prediction Power BI Dashboard**.

---

## 1. Data Connection & Data Model Architecture

### Data Sources
* **Primary Source**: MySQL Database (`customer_churn_db`) via Native MySQL Connector.
* **Secondary Source**: `powerbi/powerbi_customer_churn_dataset.csv` and `powerbi/powerbi_prediction_history.csv`.

### Star-Schema Data Model

```text
       ┌─────────────────────────┐
       │      Dim_Customers      │
       ├─────────────────────────┤
       │ customer_id (PK)        │
       │ gender, SeniorCitizen   │
       │ Contract, TenureGroup   │
       └────────────┬────────────┘
                    │ 1
                    │
                    │ *
       ┌────────────┴────────────┐          ┌─────────────────────────┐
       │    Fact_Predictions     │          │      Dim_ModelInfo      │
       ├─────────────────────────┤          ├─────────────────────────┤
       │ prediction_id (PK)      │*        1│ model_id (PK)           │
       │ customer_id (FK)        ├──────────┤ model_name, algorithm   │
       │ prediction, probability │          │ accuracy, roc_auc       │
       │ risk_level, timestamp   │          └─────────────────────────┘
       └────────────┬────────────┘
                    │ *
                    │
                    │ 1
       ┌────────────┴────────────┐
       │      Dim_Calendar       │
       ├─────────────────────────┤
       │ Date (PK), Month, Year  │
       └─────────────────────────┘
```

---

## 2. Complete DAX Measures Library

Below are the production DAX measures implemented in the report model:

```dax
// 1. Total Customers Count
Total Customers = COUNTROWS('Dim_Customers')

// 2. Total Predictions Generated
Total Predictions = COUNT('Fact_Predictions'[prediction_id])

// 3. Churn Count
Churn Count = 
CALCULATE(
    COUNT('Fact_Predictions'[prediction_id]),
    'Fact_Predictions'[prediction] = "Churn"
)

// 4. Retained Count
Retained Count = 
CALCULATE(
    COUNT('Fact_Predictions'[prediction_id]),
    'Fact_Predictions'[prediction] = "No Churn"
)

// 5. Churn Rate (%)
Churn Rate = 
DIVIDE([Churn Count], [Total Predictions], 0)

// 6. Retention Rate (%)
Retention Rate = 
1 - [Churn Rate]

// 7. Average Churn Probability
Avg Churn Probability = 
AVERAGE('Fact_Predictions'[probability])

// 8. High-Risk Customer Count
High Risk Count = 
CALCULATE(
    COUNT('Fact_Predictions'[prediction_id]),
    'Fact_Predictions'[risk_level] = "High Risk [RED]"
)

// 9. Medium-Risk Customer Count
Medium Risk Count = 
CALCULATE(
    COUNT('Fact_Predictions'[prediction_id]),
    'Fact_Predictions'[risk_level] = "Medium Risk [YELLOW]"
)

// 10. Low-Risk Customer Count
Low Risk Count = 
CALCULATE(
    COUNT('Fact_Predictions'[prediction_id]),
    'Fact_Predictions'[risk_level] = "Low Risk [GREEN]"
)

// 11. Total Monthly Revenue at Risk ($)
Revenue at Risk = 
CALCULATE(
    SUM('Dim_Customers'[monthly_charges]),
    'Fact_Predictions'[prediction] = "Churn"
)
```

---

## 3. Dashboard Pages & Visual Specifications

### 📄 Page 1: Executive Overview
* **Target Audience**: Chief Commercial Officer (CCO), VP of Customer Success.
* **Visual Elements**:
  1. **Top KPI Cards**:
     - `Total Customers`: `7,043`
     - `Churn Rate`: `26.54%` (Color-coded Red)
     - `Retention Rate`: `73.46%` (Color-coded Green)
     - `High-Risk Accounts`: `1,869`
     - `Avg Churn Probability`: `26.5%`
     - `Monthly Revenue at Risk`: `$130.6K`
  2. **Monthly Churn Probability Trend Line**: Line chart plotting prediction probabilities over time.
  3. **Risk Level Distribution**: Donut Chart displaying High Risk (Red), Medium Risk (Yellow), and Low Risk (Green) proportions.

---

### 📄 Page 2: Customer Analysis
* **Target Audience**: Customer Segmentation Analysts, Product Managers.
* **Visual Elements**:
  1. **Customer Count by Contract Type**: Clustered Column Chart (Month-to-month, 1-Year, 2-Year).
  2. **Customer Count by Internet Service**: Bar Chart (Fiber optic, DSL, No Internet).
  3. **Customer Count by Payment Method**: Horizontal Bar Chart (Electronic check, Mailed check, Bank transfer, Credit card).
  4. **Demographics Matrix**: Treemap breaking down Senior Citizen, Partner, and Dependents distribution.

---

### 📄 Page 3: Churn Driver Analysis
* **Target Audience**: Customer Retention Specialists, Pricing Analysts.
* **Visual Elements**:
  1. **Churn Rate by Contract**: Bar Chart highlighting the 42.7% churn rate in Month-to-Month contracts.
  2. **Churn Rate by Tenure Group**: Line chart showing churn drops from 47.4% (<12 months) to 6.6% (>60 months).
  3. **Monthly Charges Distribution**: Boxplot / Violin visual comparing charges for churned vs retained customers.
  4. **Top 5 Churn Drivers**: Horizontal bar chart detailing feature importances (Contract, Tenure, Fiber Optic, Electronic Check, Monthly Charges).

---

### 📄 Page 4: Prediction Analytics
* **Target Audience**: Data Scientists, Machine Learning Engineers, Operations Managers.
* **Visual Elements**:
  1. **Probability Score Histogram**: Binned distribution of output probabilities ($0.0 \to 1.0$).
  2. **Model Confidence Analysis**: Scatter plot of Churn Probability vs Model Confidence score.
  3. **Prediction Timeline**: Daily volume of queries processed by the model.

---

### 📄 Page 5: Customer Details & Action Table
* **Target Audience**: Customer Success Agents, Direct Outreach Call Centers.
* **Visual Elements**:
  - **Interactive Grid Table**:
    - `Customer ID`
    - `Prediction Outcome` (`Churn` / `No Churn`)
    - `Churn Probability (%)`
    - `Risk Tier Badge` (`High Risk`, `Medium Risk`, `Low Risk`)
    - `Contract Type`
    - `Monthly Charges ($)`
    - `Payment Method`
    - `Prediction Date`
  - **Filters**: Slicers for `Contract`, `Payment Method`, `Internet Service`, `Risk Level`, and `Date Range`.

---

## 4. Managerial Action Guide

1. **How to Identify High-Value Risk Accounts**:
   - Navigate to **Page 5 (Customer Details)**.
   - Filter `Risk Level` = `High Risk [RED]` and `Monthly Charges` > `$80.00`.
   - Export filtered list to Excel and dispatch to the VIP Customer Outreach Team for immediate contract renewal offers.
2. **How to Reduce Payment Method Churn**:
   - Review **Page 3 (Churn Analysis)** showing Electronic Check users churn at 45.3%.
   - Implement an automated campaign offering a $5 monthly bill credit for switching to Automatic Bank Transfer.

---

## 5. File Deliverables

* 📄 **[powerbi/Dashboard_Documentation.md](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/powerbi/Dashboard_Documentation.md)**: Full Power BI design documentation.
* 🐍 **[powerbi/powerbi_export_data.py](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/powerbi/powerbi_export_data.py)**: Python dataset exporter module.
* 📊 **[powerbi/powerbi_customer_churn_dataset.csv](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/powerbi/powerbi_customer_churn_dataset.csv)**: Cleaned customer dataset for Power BI.
* 📊 **[powerbi/powerbi_prediction_history.csv](file:///c:/Users/VICTUS/Documents/Customer%20Churn%20Prediction%20Analysis/powerbi/powerbi_prediction_history.csv)**: Historical predictions log for Power BI.
