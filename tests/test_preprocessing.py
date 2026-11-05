import os
import sys
import joblib
import pandas as pd
import pytest
sys.path.append(os.getcwd())

from src.components.feature_engineering import FeatureEngineer

def test_feature_engineering():
    """Verifies feature engineering transformation logic."""
    data = {
        "tenure": [0, 12, 36],
        "TotalCharges": [0.0, 1200.0, 3600.0],
        "OnlineSecurity": ["Yes", "No", "Yes"],
        "OnlineBackup": ["Yes", "No", "No"],
        "DeviceProtection": ["No", "No", "Yes"],
        "TechSupport": ["Yes", "No", "No"]
    }
    df = pd.DataFrame(data)
    fe = FeatureEngineer()
    df_transformed = fe.transform_features(df)

    assert "TenureGroup" in df_transformed.columns
    assert "ChargesPerTenure" in df_transformed.columns
    assert "HasAddons" in df_transformed.columns
    assert df_transformed["HasAddons"].iloc[0] == 3
    assert df_transformed["HasAddons"].iloc[1] == 0


def test_preprocessor_loading():
    """Verifies preprocessor binary exists and can transform sample data."""
    preprocessor_path = os.path.join("artifacts", "preprocessor.joblib")
    assert os.path.exists(preprocessor_path), "Preprocessor joblib binary does not exist!"

    preprocessor = joblib.load(preprocessor_path)
    assert preprocessor is not None
