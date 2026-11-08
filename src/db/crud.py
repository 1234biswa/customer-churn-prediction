import sys
import pandas as pd
from sqlalchemy.orm import Session
from src.db.database import Customer, Prediction, ModelInfo, ApplicationLog
from src.utils.logger import logger
from src.utils.exception import CustomException


def insert_customer(db: Session, customer_dict: dict) -> Customer:
    """Inserts a new customer record or updates existing customer attributes."""
    try:
        existing_customer = db.query(Customer).filter(Customer.customer_id == customer_dict["customer_id"]).first()
        if existing_customer:
            # Update attributes
            for key, val in customer_dict.items():
                setattr(existing_customer, key, val)
            db.commit()
            db.refresh(existing_customer)
            logger.info(f"Updated existing customer record: {customer_dict['customer_id']}")
            return existing_customer
        else:
            new_customer = Customer(**customer_dict)
            db.add(new_customer)
            db.commit()
            db.refresh(new_customer)
            logger.info(f"Inserted new customer record: {customer_dict['customer_id']}")
            return new_customer
    except Exception as e:
        db.rollback()
        logger.error(f"Error inserting/updating customer record {customer_dict.get('customer_id')}: {e}")
        raise CustomException(e, sys)


def insert_prediction(db: Session, prediction_dict: dict) -> Prediction:
    """Inserts a prediction result log for a given customer."""
    try:
        new_pred = Prediction(**prediction_dict)
        db.add(new_pred)
        db.commit()
        db.refresh(new_pred)
        logger.info(f"Inserted prediction record ID: {new_pred.prediction_id} for customer {prediction_dict['customer_id']}")
        return new_pred
    except Exception as e:
        db.rollback()
        logger.error(f"Error inserting prediction record: {e}")
        raise CustomException(e, sys)


def get_customer_by_id(db: Session, customer_id: str) -> Customer:
    """Retrieves a single customer record by customer_id."""
    try:
        return db.query(Customer).filter(Customer.customer_id == customer_id).first()
    except Exception as e:
        logger.error(f"Error fetching customer {customer_id}: {e}")
        raise CustomException(e, sys)


def get_prediction_history(db: Session, limit: int = 100) -> pd.DataFrame:
    """Retrieves merged prediction history with customer features as a Pandas DataFrame."""
    try:
        query = (
            db.query(
                Prediction.prediction_id,
                Prediction.customer_id,
                Customer.gender,
                Customer.tenure,
                Customer.contract,
                Customer.monthly_charges,
                Prediction.probability,
                Prediction.prediction,
                Prediction.risk_level,
                Prediction.prediction_time
            )
            .join(Customer, Prediction.customer_id == Customer.customer_id)
            .order_by(Prediction.prediction_time.desc())
            .limit(limit)
        )
        results = query.all()
        if not results:
            return pd.DataFrame()

        data = [
            {
                "Prediction ID": r.prediction_id,
                "Customer ID": r.customer_id,
                "Gender": r.gender,
                "Tenure (Mo)": r.tenure,
                "Contract": r.contract,
                "Monthly Charges": f"${r.monthly_charges:.2f}",
                "Churn Probability": f"{r.probability * 100:.2f}%",
                "Prediction": r.prediction,
                "Risk Level": r.risk_level,
                "Timestamp": r.prediction_time.strftime("%Y-%m-%d %H:%M:%S") if r.prediction_time else ""
            }
            for r in results
        ]
        return pd.DataFrame(data)

    except Exception as e:
        logger.error(f"Error retrieving prediction history: {e}")
        raise CustomException(e, sys)


def update_customer(db: Session, customer_id: str, update_dict: dict) -> Customer:
    """Updates selected attributes for an existing customer."""
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            raise ValueError(f"Customer {customer_id} not found for update.")
        for key, value in update_dict.items():
            setattr(customer, key, value)
        db.commit()
        db.refresh(customer)
        logger.info(f"Successfully updated customer {customer_id}")
        return customer
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update customer {customer_id}: {e}")
        raise CustomException(e, sys)


def delete_customer(db: Session, customer_id: str) -> bool:
    """Deletes a customer record and cascade deletes associated predictions."""
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            return False
        db.delete(customer)
        db.commit()
        logger.info(f"Deleted customer {customer_id} and associated predictions.")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting customer {customer_id}: {e}")
        raise CustomException(e, sys)


def list_all_customers(db: Session) -> list[Customer]:
    """Retrieves all registered customer records."""
    try:
        return db.query(Customer).all()
    except Exception as e:
        logger.error(f"Error listing customers: {e}")
        raise CustomException(e, sys)


def log_application_event(db: Session, event_type: str, description: str, status: str = "SUCCESS") -> ApplicationLog:
    """Logs system and application events into application_logs table."""
    try:
        log_entry = ApplicationLog(event_type=event_type, description=description, status=status)
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        return log_entry
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to record application log: {e}")
        return None
