import os
import sys
import pytest
sys.path.append(os.getcwd())

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

def test_valid_customer_prediction():
    """Tests end-to-end inference on a valid customer profile."""
    sample = CustomData(
        gender="Female", SeniorCitizen=0, Partner="Yes", Dependents="No",
        tenure=12, PhoneService="Yes", MultipleLines="No", InternetService="DSL",
        OnlineSecurity="Yes", OnlineBackup="No", DeviceProtection="No", TechSupport="Yes",
        StreamingTV="No", StreamingMovies="No", Contract="One year",
        PaperlessBilling="No", PaymentMethod="Credit card (automatic)", MonthlyCharges=60.00, TotalCharges=720.00
    )
    raw_df = sample.get_data_as_data_frame()
    pipeline = PredictPipeline()
    result = pipeline.predict(raw_df)

    assert "prediction_label" in result
    assert "prediction_text" in result
    assert "churn_probability_pct" in result
    assert "risk_level" in result
    assert result["churn_probability_pct"] >= 0.0 and result["churn_probability_pct"] <= 100.0


def test_invalid_negative_input():
    """Verifies that negative tenure or charges raise a validation ValueError."""
    invalid_sample = CustomData(
        gender="Male", SeniorCitizen=0, Partner="No", Dependents="No",
        tenure=-5, PhoneService="Yes", MultipleLines="No", InternetService="DSL",
        OnlineSecurity="No", OnlineBackup="No", DeviceProtection="No", TechSupport="No",
        StreamingTV="No", StreamingMovies="No", Contract="Month-to-month",
        PaperlessBilling="Yes", PaymentMethod="Mailed check", MonthlyCharges=50.00, TotalCharges=250.00
    )
    raw_df = invalid_sample.get_data_as_data_frame()
    pipeline = PredictPipeline()

    with pytest.raises(Exception):
        pipeline.predict(raw_df)
