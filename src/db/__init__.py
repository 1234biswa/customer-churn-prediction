"""
Database Package containing SQLAlchemy engine connection, ORM models, and CRUD operations.
"""
from src.db.connection import engine, SessionLocal, get_db_session
from src.db.database import Base, Customer, Prediction, ModelInfo, ApplicationLog, init_db
from src.db.crud import (
    insert_customer,
    insert_prediction,
    get_customer_by_id,
    get_prediction_history,
    update_customer,
    delete_customer,
    list_all_customers,
    log_application_event,
)

__all__ = [
    "engine",
    "SessionLocal",
    "get_db_session",
    "Base",
    "Customer",
    "Prediction",
    "ModelInfo",
    "ApplicationLog",
    "init_db",
    "insert_customer",
    "insert_prediction",
    "get_customer_by_id",
    "get_prediction_history",
    "update_customer",
    "delete_customer",
    "list_all_customers",
    "log_application_event",
]
