import os
import sys
import datetime
sys.path.append(os.getcwd())

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.utils.styles import apply_custom_css
from src.db import (
    init_db,
    SessionLocal,
    insert_customer,
    insert_prediction,
    get_prediction_history,
    log_application_event
)

# Initialize Database Schema
try:
    init_db()
except Exception as e:
    st.warning(f"Database Initialization Notice: {e}")

# Configure Page Config
st.set_page_config(
    page_title="ChurnGuard Enterprise | AI Churn Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Custom Styles
apply_custom_css()

# Sidebar Navigation
st.sidebar.markdown("## 📊 **ChurnGuard Enterprise**")
st.sidebar.caption("AI-Powered Customer Retention Platform v1.0")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate Module:",
    [
        "🏠 Home",
        "🎯 Single Customer Prediction",
        "📈 Analytics Dashboard",
        "📜 Prediction History",
        "ℹ️ About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Model Status**: Champion Gradient Boosting Classifier loaded (Accuracy: 80.48%, ROC-AUC: 0.8438)."
)

# -----------------------------------------------------------------------------
# 1. HOME PAGE
# -----------------------------------------------------------------------------
if page == "🏠 Home":
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">Customer Churn Prediction Analysis</div>
            <div class="hero-subtitle">
                An enterprise ML application for predicting customer retention risk, identifying key drivers, 
                and recommending proactive business interventions before cancellation occurs.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Key Statistics Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">7,043</div>
                <div class="metric-label">Analyzed Profiles</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">80.48%</div>
                <div class="metric-label">Model Accuracy</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">0.8438</div>
                <div class="metric-label">ROC-AUC Score</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">2.39 ms</div>
                <div class="metric-label">Inference Latency</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 💼 Business Problem")
        st.write("""
        Acquiring new customers costs **5x to 25x more** than retaining existing ones. Silent customer churn 
        gradually erodes Monthly Recurring Revenue (MRR). This application shifts organizations from reactive 
        win-back campaigns to proactive retention alerts.
        """)

        st.markdown("### 🎯 Key Objectives")
        st.markdown("""
        * **Predictive Precision**: Calculate continuous churn risk probability (0% to 100%).
        * **Risk Stratification**: Categorize accounts into Low, Medium, and High Risk tiers.
        * **Explainable AI**: Highlight key service drivers (e.g. Month-to-Month contracts, Fiber Optic, High Monthly Fees).
        * **Actionable Guidance**: Recommend targeted retention strategies based on risk profile.
        """)

    with col_right:
        st.markdown("### 🛠️ Technology Stack")
        st.markdown("""
        * **Machine Learning**: Gradient Boosting Classifier, Scikit-Learn, XGBoost
        * **Database & Persistence**: MySQL / SQLite, SQLAlchemy ORM, PyMySQL
        * **Frontend Dashboard**: Streamlit, Custom SaaS CSS, Plotly
        * **Testing & MLOps**: Pytest, Docker, Dual-Logging Engine
        """)

        st.markdown("### 🏆 Champion Model Performance")
        st.markdown("""
        * **Model**: Gradient Boosting Classifier
        * **Accuracy**: 80.48%
        * **F1 Score**: 0.5914
        * **Recall**: 53.21%
        * **ROC-AUC**: 0.8438
        """)

# -----------------------------------------------------------------------------
# 2. SINGLE CUSTOMER PREDICTION PAGE
# -----------------------------------------------------------------------------
elif page == "🎯 Single Customer Prediction":
    st.title("🎯 Single Customer Churn Risk Calculator")
    st.caption("Enter customer demographic, subscription, and billing details to generate real-time churn risk score.")

    with st.form("prediction_form"):
        st.markdown('<div class="form-section-header">👤 Demographic & Personal Profile</div>', unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            gender = st.selectbox("Gender", ["Female", "Male"])
        with col2:
            senior_citizen = st.selectbox("Senior Citizen", [0, 1], format_func=lambda x: "Yes (65+)" if x == 1 else "No (<65)")
        with col3:
            partner = st.selectbox("Has Partner", ["No", "Yes"])
        with col4:
            dependents = st.selectbox("Has Dependents", ["No", "Yes"])

        st.markdown('<div class="form-section-header">🌐 Subscribed Services</div>', unsafe_allow_html=True)
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        with col6:
            multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        with col7:
            internet_service = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
        with col8:
            online_security = st.selectbox("Online Security Add-on", ["No", "Yes", "No internet service"])

        col9, col10, col11, col12 = st.columns(4)
        with col9:
            online_backup = st.selectbox("Online Backup Add-on", ["No", "Yes", "No internet service"])
        with col10:
            device_protection = st.selectbox("Device Protection Add-on", ["No", "Yes", "No internet service"])
        with col11:
            tech_support = st.selectbox("Tech Support Add-on", ["No", "Yes", "No internet service"])
        with col12:
            streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])

        st.markdown('<div class="form-section-header">💳 Account, Contract & Billing Info</div>', unsafe_allow_html=True)
        col13, col14, col15 = st.columns(3)
        with col13:
            streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
        with col14:
            contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        with col15:
            paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])

        col16, col17, col18 = st.columns(3)
        with col16:
            payment_method = st.selectbox("Payment Method", [
                "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
            ])
        with col17:
            tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=12, step=1)
        with col18:
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=200.0, value=75.0, step=0.5)

        total_charges = st.number_input(
            "Estimated Total Charges ($)",
            min_value=0.0,
            value=float(round(tenure * monthly_charges, 2)),
            step=10.0
        )

        submit_button = st.form_submit_button("🚀 Generate Churn Risk Score")

    if submit_button:
        try:
            cust_id = f"CUST-{datetime.datetime.now().strftime('%H%M%S')}"
            custom_data = CustomData(
                gender=gender,
                SeniorCitizen=senior_citizen,
                Partner=partner,
                Dependents=dependents,
                tenure=tenure,
                PhoneService=phone_service,
                MultipleLines=multiple_lines,
                InternetService=internet_service,
                OnlineSecurity=online_security,
                OnlineBackup=online_backup,
                DeviceProtection=device_protection,
                TechSupport=tech_support,
                StreamingTV=streaming_tv,
                StreamingMovies=streaming_movies,
                Contract=contract,
                PaperlessBilling=paperless_billing,
                PaymentMethod=payment_method,
                MonthlyCharges=monthly_charges,
                TotalCharges=total_charges,
                customerID=cust_id
            )

            raw_df = custom_data.get_data_as_data_frame()
            pipeline = PredictPipeline()
            res = pipeline.predict(raw_df)

            # Insert Customer & Prediction into Database
            db = SessionLocal()
            try:
                insert_customer(db, {
                    "customer_id": cust_id,
                    "gender": gender,
                    "senior_citizen": senior_citizen,
                    "partner": partner,
                    "dependents": dependents,
                    "tenure": tenure,
                    "phone_service": phone_service,
                    "internet_service": internet_service,
                    "contract": contract,
                    "payment_method": payment_method,
                    "monthly_charges": monthly_charges,
                    "total_charges": total_charges
                })

                insert_prediction(db, {
                    "customer_id": cust_id,
                    "prediction": res["prediction_text"],
                    "probability": float(res["churn_probability_pct"] / 100.0),
                    "risk_level": res["risk_level"],
                    "confidence_score": float(1.0 - (res["churn_probability_pct"] / 100.0) if res["prediction_text"] == "No Churn" else res["churn_probability_pct"] / 100.0),
                    "model_name": "Gradient Boosting Classifier"
                })

                log_application_event(db, "Prediction Generated", f"Generated churn score for {cust_id}: {res['churn_probability_pct']}% ({res['risk_level']})")
            finally:
                db.close()

            st.markdown("---")
            st.subheader("📊 Prediction Results & Churn Assessment")

            res_col1, res_col2 = st.columns([1, 1])

            with res_col1:
                # Gauge Chart via Plotly
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=res["churn_probability_pct"],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Churn Probability (%)", 'font': {'size': 18}},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#3b82f6"},
                        'steps': [
                            {'range': [0, 30], 'color': "#064e3b"},
                            {'range': [30, 65], 'color': "#78350f"},
                            {'range': [65, 100], 'color': "#7f1d1d"}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 4},
                            'thickness': 0.75,
                            'value': res["churn_probability_pct"]
                        }
                    }
                ))
                fig.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)

            with res_col2:
                st.markdown(f"### Outcome: **{res['prediction_text']}**")
                st.markdown(f"**Assigned Risk Tier**: {res['risk_level']}")
                st.progress(res["churn_probability_pct"] / 100.0)

                st.markdown("#### 💡 Strategic Business Recommendation")
                if res["churn_probability_pct"] >= 65:
                    st.error("🚨 **High Risk Warning**: Customer requires immediate intervention! Offer a 15% discount for committing to a 1-Year or 2-Year contract and assign a Customer Success agent.")
                elif res["churn_probability_pct"] >= 30:
                    st.warning("🟡 **Moderate Risk Warning**: Customer shows signs of vulnerability. Recommend bundling TechSupport & OnlineSecurity or promoting automatic bank transfer billing.")
                else:
                    st.success("🟢 **Low Risk Profile**: Customer is stable and satisfied. Excellent candidate for loyalty rewards or upsell programs.")

        except Exception as e:
            st.error(f"Prediction Error: {e}")

# -----------------------------------------------------------------------------
# 3. ANALYTICS DASHBOARD PAGE
# -----------------------------------------------------------------------------
elif page == "📈 Analytics Dashboard":
    st.title("📈 Executive Analytics & Risk Dashboard")
    st.caption("Live metrics and churn distribution insights derived from persistent database records.")

    db = SessionLocal()
    try:
        history_df = get_prediction_history(db, limit=500)
    finally:
        db.close()

    if history_df.empty:
        st.info("No prediction history recorded in the database yet. Generate predictions on the Single Customer Prediction page.")
    else:
        # KPI Summary Row
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        total_preds = len(history_df)
        high_risk_count = len(history_df[history_df["Risk Level"].str.contains("High")])
        med_risk_count = len(history_df[history_df["Risk Level"].str.contains("Medium")])
        low_risk_count = len(history_df[history_df["Risk Level"].str.contains("Low")])

        with kpi1:
            st.metric("Total DB Predictions", total_preds)
        with kpi2:
            st.metric("High Risk Accounts", high_risk_count, delta=f"{high_risk_count/total_preds:.0%}" if total_preds else "0%")
        with kpi3:
            st.metric("Medium Risk Accounts", med_risk_count)
        with kpi4:
            st.metric("Low Risk Accounts", low_risk_count)

        st.markdown("---")

        dash_col1, dash_col2 = st.columns(2)

        with dash_col1:
            st.subheader("Risk Tier Distribution")
            risk_counts = history_df["Risk Level"].value_counts().reset_index()
            risk_counts.columns = ["Risk Tier", "Count"]
            fig_pie = px.pie(
                risk_counts, values="Count", names="Risk Tier",
                color="Risk Tier",
                color_discrete_map={
                    "High Risk [RED]": "#ef4444",
                    "Medium Risk [YELLOW]": "#f59e0b",
                    "Low Risk [GREEN]": "#10b981"
                },
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with dash_col2:
            st.subheader("Churn Risk by Contract Type")
            fig_bar = px.histogram(
                history_df, x="Contract", color="Prediction",
                barmode="group",
                color_discrete_map={"Churn": "#ef4444", "No Churn": "#10b981"}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# 4. PREDICTION HISTORY PAGE
# -----------------------------------------------------------------------------
elif page == "📜 Prediction History":
    st.title("📜 Database Prediction History & Audit Logs")
    st.caption("Searchable table fetching records directly from the relational database.")

    db = SessionLocal()
    try:
        history_df = get_prediction_history(db, limit=500)
    finally:
        db.close()

    if history_df.empty:
        st.info("No prediction history recorded in the database yet.")
    else:
        search_query = st.text_input("🔍 Search by Customer ID or Contract:", "")
        if search_query:
            filtered_df = history_df[
                history_df["Customer ID"].str.contains(search_query, case=False) |
                history_df["Contract"].str.contains(search_query, case=False)
            ]
        else:
            filtered_df = history_df

        st.dataframe(filtered_df, use_container_width=True)

        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Prediction Logs to CSV",
            data=csv_data,
            file_name=f"churn_prediction_db_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

# -----------------------------------------------------------------------------
# 5. ABOUT PROJECT PAGE
# -----------------------------------------------------------------------------
elif page == "ℹ️ About Project":
    st.title("ℹ️ About ChurnGuard Enterprise")

    st.markdown("""
    ### 📌 Project Overview
    **Customer Churn Prediction Analysis** is an end-to-end Machine Learning web application engineered 
    to forecast customer attrition probabilities and help businesses retain high-value accounts.

    ### 🔄 System Architecture Workflow
    ```text
    User Inputs (UI / Form)
           │
           ▼
    CustomData Formatter
           │
           ▼
    Feature Engineering (TenureGroup, ChargesPerTenure, HasAddons)
           │
           ▼
    Scikit-Learn ColumnTransformer (StandardScaler + OneHotEncoder)
           │
           ▼
    Champion Gradient Boosting Classifier (predict_proba)
           │
           ▼
    Risk Level Categorization (Low / Medium / High Risk)
           │
           ▼
    Relational Database Persistence (customers, predictions, application_logs)
    ```

    ### ⚙️ Pipeline Specifications
    * **Algorithm**: Gradient Boosting Classifier (`n_estimators=100`, `learning_rate=0.1`)
    * **Evaluation Benchmark**: ROC-AUC Score = **0.8438**, Accuracy = **80.48%**
    * **Database Layer**: MySQL / SQLite with SQLAlchemy ORM and PyMySQL
    * **Artifact Serialization**: `best_model.joblib` and `preprocessor.joblib`

    ### 🚀 Future Roadmap (Phase 11)
    * Automated Email & Slack alerts for high-risk customer accounts.
    * REST API engine powered by FastAPI (`/predict` & `/health` endpoints).
    * Production containerization via Docker and Kubernetes cloud hosting.
    """)

