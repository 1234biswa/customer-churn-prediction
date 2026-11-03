# ❓ Frequently Asked Questions (FAQ)

Here are answers to the top 20+ questions about the **Customer Churn Prediction Analysis (ChurnGuard Enterprise)** platform.

---

### 🧠 Data Science & Machine Learning Questions

#### 1. What is Customer Churn?
Customer churn occurs when a customer cancels their subscription or stops doing business with a company.

#### 2. Why is predicting churn important?
Acquiring new customers is **5x to 25x more expensive** than retaining existing ones. Predicting churn allows companies to intervene proactively.

#### 3. What dataset is used in this project?
We use the IBM Telco Customer Churn dataset containing **7,043 customer profiles** with 21 demographic, service, and billing attributes.

#### 4. Which Machine Learning algorithms were evaluated?
We evaluated 5 algorithms: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting Classifier, and XGBoost.

#### 5. Which model was selected as the Champion Model?
**Gradient Boosting Classifier**, achieving an **Accuracy of 80.48%** and **ROC-AUC Score of 0.8438**.

#### 6. What is ROC-AUC?
ROC-AUC measures a binary classifier's ability to distinguish between classes (Churn vs. No Churn) across all decision thresholds. A score of 0.8438 indicates strong predictive power.

#### 7. How are churn probability scores converted into risk tiers?
Probabilities are mapped to 3 tiers: **Low Risk (0-30%)**, **Medium Risk (31-65%)**, and **High Risk (66-100%)**.

---

### ⚙️ Feature Engineering & Preprocessing Questions

#### 8. What feature engineering transformations were performed?
We engineered 3 key features: `TenureGroup` (binned tenure), `ChargesPerTenure` (monthly ratio), and `HasAddons` (security add-on count).

#### 9. How are categorical variables handled?
Categorical columns are transformed using Scikit-Learn's `OneHotEncoder`.

#### 10. How are numerical variables scaled?
Numerical features (`tenure`, `MonthlyCharges`, `TotalCharges`) are standardized using `StandardScaler`.

---

### 🗄️ Database & Persistence Questions

#### 11. What database is used in this project?
The project supports **MySQL** for production and features an automatic **SQLite fallback engine** (`data/customer_churn_db.sqlite`) for local development.

#### 12. How does the application connect to the database?
Through **SQLAlchemy ORM** and **PyMySQL**, using object-relational models defined in `src/db/database.py`.

#### 13. Are prediction queries saved automatically?
Yes! Every single prediction submitted through the Streamlit web form is automatically recorded in the database `predictions` table.

---

### 🌐 Streamlit & Web UI Questions

#### 14. How do I launch the Streamlit app?
Run `streamlit run app.py` in your terminal.

#### 15. Can I export prediction history to CSV?
Yes, the **Prediction History** page includes a 1-click **📥 Export Prediction Logs to CSV** button.

#### 16. How is custom styling applied to Streamlit?
Custom CSS rules are injected via `src/utils/styles.py` to deliver a modern dark-mode SaaS UI.

---

### ☁️ Deployment & DevOps Questions

#### 17. Where can this app be deployed?
Primary target is **Streamlit Community Cloud** (`share.streamlit.io`); secondary target is **Render**.

#### 18. How are database credentials protected in the cloud?
Credentials are standard environment variables managed securely through Streamlit Cloud Secrets.

#### 19. How do I run automated unit tests?
Run `python -m pytest tests/` in your terminal.

#### 20. What is the average inference latency?
The average end-to-end inference latency is **`84.75 ms`**.
