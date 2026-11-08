import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
import joblib

from src.utils.logger import logger
from src.utils.exception import CustomException
from src.components.feature_engineering import FeatureEngineer


class CustomData:
    """
    Data holder class responsible for collecting raw customer inputs
    and converting them into a structured Pandas DataFrame.
    """

    def __init__(
        self,
        gender: str,
        SeniorCitizen: int,
        Partner: str,
        Dependents: str,
        tenure: int,
        PhoneService: str,
        MultipleLines: str,
        InternetService: str,
        OnlineSecurity: str,
        OnlineBackup: str,
        DeviceProtection: str,
        TechSupport: str,
        StreamingTV: str,
        StreamingMovies: str,
        Contract: str,
        PaperlessBilling: str,
        PaymentMethod: str,
        MonthlyCharges: float,
        TotalCharges: float,
        customerID: str = "SAMPLE-ID-0000"
    ):
        self.customerID = customerID
        self.gender = gender
        self.SeniorCitizen = SeniorCitizen
        self.Partner = Partner
        self.Dependents = Dependents
        self.tenure = tenure
        self.PhoneService = PhoneService
        self.MultipleLines = MultipleLines
        self.InternetService = InternetService
        self.OnlineSecurity = OnlineSecurity
        self.OnlineBackup = OnlineBackup
        self.DeviceProtection = DeviceProtection
        self.TechSupport = TechSupport
        self.StreamingTV = StreamingTV
        self.StreamingMovies = StreamingMovies
        self.Contract = Contract
        self.PaperlessBilling = PaperlessBilling
        self.PaymentMethod = PaymentMethod
        self.MonthlyCharges = MonthlyCharges
        self.TotalCharges = TotalCharges

    def get_data_as_data_frame(self) -> pd.DataFrame:
        """Converts internal attributes into a single-row DataFrame."""
        try:
            custom_data_dict = {
                "customerID": [self.customerID],
                "gender": [self.gender],
                "SeniorCitizen": [self.SeniorCitizen],
                "Partner": [self.Partner],
                "Dependents": [self.Dependents],
                "tenure": [self.tenure],
                "PhoneService": [self.PhoneService],
                "MultipleLines": [self.MultipleLines],
                "InternetService": [self.InternetService],
                "OnlineSecurity": [self.OnlineSecurity],
                "OnlineBackup": [self.OnlineBackup],
                "DeviceProtection": [self.DeviceProtection],
                "TechSupport": [self.TechSupport],
                "StreamingTV": [self.StreamingTV],
                "StreamingMovies": [self.StreamingMovies],
                "Contract": [self.Contract],
                "PaperlessBilling": [self.PaperlessBilling],
                "PaymentMethod": [self.PaymentMethod],
                "MonthlyCharges": [self.MonthlyCharges],
                "TotalCharges": [self.TotalCharges],
            }
            return pd.DataFrame(custom_data_dict)
        except Exception as e:
            logger.error("Error creating DataFrame from CustomData!")
            raise CustomException(e, sys)


class PredictPipeline:
    """
    Reusable prediction pipeline component that loads preprocessor and model binaries,
    applies feature transformations, validates inputs, and calculates churn risk scores.
    """

    def __init__(
        self,
        model_path: str = os.path.join("artifacts", "best_model.joblib"),
        preprocessor_path: str = os.path.join("artifacts", "preprocessor.joblib")
    ):
        self.model_path = model_path
        self.preprocessor_path = preprocessor_path

    def classify_risk(self, probability: float) -> str:
        """
        Maps probability score (0.0 to 1.0) into discrete risk levels:
        - Probability < 0.30 -> Low Risk
        - 0.30 <= Probability < 0.65 -> Medium Risk
        - Probability >= 0.65 -> High Risk
        """
        if probability < 0.30:
            return "Low Risk [GREEN]"
        elif probability < 0.65:
            return "Medium Risk [YELLOW]"
        else:
            return "High Risk [RED]"

    def validate_input(self, df: pd.DataFrame):
        """Validates that input DataFrame contains required numeric constraints."""
        if df["tenure"].iloc[0] < 0:
            raise ValueError("Invalid Input: tenure cannot be negative.")
        if df["MonthlyCharges"].iloc[0] < 0 or df["TotalCharges"].iloc[0] < 0:
            raise ValueError("Invalid Input: charges cannot be negative.")

    def predict(self, raw_df: pd.DataFrame) -> dict:
        """
        Executes end-to-end prediction workflow on raw input DataFrame.

        Returns:
            dict containing prediction_label, prediction_text, churn_probability %, and risk_level.
        """
        logger.info("Starting Prediction Pipeline execution...")
        try:
            # 1. Validate Input
            self.validate_input(raw_df)
            logger.info("Validating Input... PASSED")

            # 2. Apply Feature Engineering
            logger.info("Transforming Features...")
            fe = FeatureEngineer()
            df_fe = fe.transform_features(raw_df)

            # Drop primary key if present
            if "customerID" in df_fe.columns:
                df_fe.drop(columns=["customerID"], inplace=True)

            # 3. Load Artifacts
            logger.info(f"Loading Preprocessor from: {self.preprocessor_path}")
            preprocessor = joblib.load(self.preprocessor_path)

            logger.info(f"Loading Model from: {self.model_path}")
            model = joblib.load(self.model_path)

            # 4. Transform Features using Preprocessor
            scaled_data_arr = preprocessor.transform(df_fe)

            # Convert to DataFrame with feature names to match model input features
            cat_encoder = preprocessor.named_transformers_["cat_pipeline"].named_steps["one_hot_encoder"]
            num_cols = list(df_fe.select_dtypes(include=["int64", "float64"]).columns)
            cat_cols = list(df_fe.select_dtypes(include=["object", "category", "string"]).columns)
            encoded_cat_names = list(cat_encoder.get_feature_names_out(cat_cols))
            feature_names = num_cols + encoded_cat_names

            scaled_df = pd.DataFrame(scaled_data_arr, columns=feature_names)

            # 5. Generate Probability & Prediction
            logger.info("Generating Prediction...")
            prob = model.predict_proba(scaled_df)[0, 1]
            prediction_label = int(prob >= 0.50)
            prediction_text = "Churn" if prediction_label == 1 else "No Churn"
            risk_level = self.classify_risk(prob)

            logger.info(f"Prediction Completed Successfully. Probability: {prob:.4f}, Risk: {risk_level}")

            return {
                "prediction_label": prediction_label,
                "prediction_text": prediction_text,
                "churn_probability_pct": round(prob * 100, 2),
                "risk_level": risk_level
            }

        except Exception as e:
            logger.error("Error encountered during Prediction Pipeline execution!")
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        pipeline = PredictPipeline()

        # Define 5 Sample Customers representing different risk profiles
        samples = [
            ("Sample 1: High Risk Month-to-Month Fiber User", CustomData(
                gender="Female", SeniorCitizen=0, Partner="No", Dependents="No",
                tenure=1, PhoneService="Yes", MultipleLines="No", InternetService="Fiber optic",
                OnlineSecurity="No", OnlineBackup="No", DeviceProtection="No", TechSupport="No",
                StreamingTV="Yes", StreamingMovies="Yes", Contract="Month-to-month",
                PaperlessBilling="Yes", PaymentMethod="Electronic check", MonthlyCharges=95.50, TotalCharges=95.50
            )),
            ("Sample 2: Low Risk Long-Term 2-Year Contract Loyalist", CustomData(
                gender="Male", SeniorCitizen=0, Partner="Yes", Dependents="Yes",
                tenure=65, PhoneService="Yes", MultipleLines="Yes", InternetService="DSL",
                OnlineSecurity="Yes", OnlineBackup="Yes", DeviceProtection="Yes", TechSupport="Yes",
                StreamingTV="No", StreamingMovies="No", Contract="Two year",
                PaperlessBilling="No", PaymentMethod="Bank transfer (automatic)", MonthlyCharges=64.00, TotalCharges=4160.00
            )),
            ("Sample 3: Medium Risk 1-Year Contract Fiber User", CustomData(
                gender="Female", SeniorCitizen=1, Partner="No", Dependents="No",
                tenure=14, PhoneService="Yes", MultipleLines="Yes", InternetService="Fiber optic",
                OnlineSecurity="No", OnlineBackup="Yes", DeviceProtection="No", TechSupport="No",
                StreamingTV="Yes", StreamingMovies="No", Contract="One year",
                PaperlessBilling="Yes", PaymentMethod="Credit card (automatic)", MonthlyCharges=88.20, TotalCharges=1234.80
            )),
            ("Sample 4: Low Risk Basic Phone-Only Subscriber", CustomData(
                gender="Male", SeniorCitizen=0, Partner="No", Dependents="No",
                tenure=40, PhoneService="Yes", MultipleLines="No", InternetService="No",
                OnlineSecurity="No internet service", OnlineBackup="No internet service",
                DeviceProtection="No internet service", TechSupport="No internet service",
                StreamingTV="No internet service", StreamingMovies="No internet service",
                Contract="Two year", PaperlessBilling="No", PaymentMethod="Mailed check", MonthlyCharges=20.05, TotalCharges=802.00
            )),
            ("Sample 5: High Risk Senior Citizen Electronic Check User", CustomData(
                gender="Female", SeniorCitizen=1, Partner="No", Dependents="No",
                tenure=3, PhoneService="Yes", MultipleLines="Yes", InternetService="Fiber optic",
                OnlineSecurity="No", OnlineBackup="No", DeviceProtection="No", TechSupport="No",
                StreamingTV="Yes", StreamingMovies="Yes", Contract="Month-to-month",
                PaperlessBilling="Yes", PaymentMethod="Electronic check", MonthlyCharges=102.00, TotalCharges=306.00
            ))
        ]

        print("\n" + "="*85)
        print("                     SAMPLE CUSTOMER CHURN PREDICTIONS")
        print("="*85)

        for label, sample_data in samples:
            raw_df = sample_data.get_data_as_data_frame()
            res = pipeline.predict(raw_df)
            print(f"\n* {label}")
            print(f"   - Prediction:        {res['prediction_text']} (Label: {res['prediction_label']})")
            print(f"   - Churn Probability: {res['churn_probability_pct']}%")
            print(f"   - Assigned Risk:     {res['risk_level']}")

        print("\n" + "="*85)

    except Exception as e:
        print(f"Prediction Pipeline Test Failed: {e}")
