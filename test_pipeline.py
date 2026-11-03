import os
import sys
import pytest
sys.path.append(os.getcwd())

from src.pipeline.predict_pipeline import PredictPipeline

def test_pipeline_risk_classification():
    """Verifies probability risk tier mapping thresholds."""
    pipeline = PredictPipeline()

    assert "Low Risk" in pipeline.classify_risk(0.15)
    assert "Medium Risk" in pipeline.classify_risk(0.45)
    assert "High Risk" in pipeline.classify_risk(0.85)


def test_missing_artifacts_error_handling():
    """Verifies pipeline raises custom exception if artifact paths are invalid."""
    fake_pipeline = PredictPipeline(
        model_path="artifacts/non_existent_model.joblib",
        preprocessor_path="artifacts/preprocessor.joblib"
    )
    import pandas as pd
    df = pd.DataFrame({"tenure": [10], "MonthlyCharges": [50.0], "TotalCharges": [500.0]})

    with pytest.raises(Exception):
        fake_pipeline.predict(df)
