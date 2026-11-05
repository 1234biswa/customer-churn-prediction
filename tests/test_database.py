import os
import sys
import pytest
sys.path.append(os.getcwd())

from src.db import (
    init_db,
    SessionLocal,
    insert_customer,
    insert_prediction,
    get_customer_by_id,
    get_prediction_history,
    update_customer,
    delete_customer,
    log_application_event
)

@pytest.fixture(scope="module")
def db_session():
    """Fixture initializing database schema and yielding session."""
    init_db()
    session = SessionLocal()
    yield session
    session.close()


def test_customer_crud_flow(db_session):
    """Verifies complete Insert, Read, Update, and Delete flow for Customer table."""
    cust_data = {
        "customer_id": "TEST-QA-999",
        "gender": "Male",
        "senior_citizen": 0,
        "partner": "No",
        "dependents": "No",
        "tenure": 5,
        "phone_service": "Yes",
        "internet_service": "Fiber optic",
        "contract": "Month-to-month",
        "payment_method": "Electronic check",
        "monthly_charges": 85.00,
        "total_charges": 425.00
    }

    # 1. Insert
    c = insert_customer(db_session, cust_data)
    assert c.customer_id == "TEST-QA-999"

    # 2. Read
    fetched = get_customer_by_id(db_session, "TEST-QA-999")
    assert fetched is not None
    assert fetched.monthly_charges == 85.00

    # 3. Update
    updated = update_customer(db_session, "TEST-QA-999", {"monthly_charges": 90.00})
    assert updated.monthly_charges == 90.00

    # 4. Insert Prediction
    pred_data = {
        "customer_id": "TEST-QA-999",
        "prediction": "Churn",
        "probability": 0.7850,
        "risk_level": "High Risk [RED]",
        "confidence_score": 0.7850,
        "model_name": "Gradient Boosting"
    }
    p = insert_prediction(db_session, pred_data)
    assert p.prediction_id is not None

    # 5. Read Prediction History
    hist = get_prediction_history(db_session, limit=10)
    assert not hist.empty

    # 6. Delete
    deleted = delete_customer(db_session, "TEST-QA-999")
    assert deleted is True
    assert get_customer_by_id(db_session, "TEST-QA-999") is None


def test_application_logging(db_session):
    """Verifies application event logging into application_logs table."""
    log_entry = log_application_event(db_session, "Unit Test Event", "Executing Pytest suite")
    assert log_entry is not None
    assert log_entry.event_type == "Unit Test Event"
