import os
import sys
import joblib
import pandas as pd
import numpy as np
import pytest
sys.path.append(os.getcwd())

def test_model_loading_and_prediction():
    """Verifies best_model.joblib binary exists, loads, and outputs valid probability scores."""
    model_path = os.path.join("artifacts", "best_model.joblib")
    assert os.path.exists(model_path), "Model joblib binary does not exist!"

    model = joblib.load(model_path)
    assert hasattr(model, "predict_proba")

    X_test_path = os.path.join("artifacts", "X_test.csv")
    assert os.path.exists(X_test_path), "X_test.csv artifact does not exist!"

    X_test = pd.read_csv(X_test_path)
    probs = model.predict_proba(X_test.head(5))[:, 1]

    assert len(probs) == 5
    assert np.all(probs >= 0.0) and np.all(probs <= 1.0)
