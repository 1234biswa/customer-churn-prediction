import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

from src.db.connection import engine
from src.utils.logger import logger

Base = declarative_base()


class User(Base):
    """Application account. Passwords are stored only as bcrypt hashes."""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(254), nullable=False, unique=True, index=True)
    password_hash = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class UserCustomer(Base):
    """Ownership mapping used to isolate each account's prediction history."""
    __tablename__ = "user_customers"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)


class Customer(Base):
    """SQLAlchemy ORM model for storing customer profiles."""
    __tablename__ = "customers"

    customer_id = Column(String(50), primary_key=True)
    gender = Column(String(10), nullable=False)
    senior_citizen = Column(Integer, nullable=False, default=0)
    partner = Column(String(5), nullable=False)
    dependents = Column(String(5), nullable=False)
    tenure = Column(Integer, nullable=False, default=0)
    phone_service = Column(String(5), nullable=False)
    internet_service = Column(String(20), nullable=False)
    contract = Column(String(20), nullable=False)
    payment_method = Column(String(50), nullable=False)
    monthly_charges = Column(Float, nullable=False)
    total_charges = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)

    predictions = relationship("Prediction", back_populates="customer", cascade="all, delete-orphan")


class Prediction(Base):
    """SQLAlchemy ORM model for storing model prediction history."""
    __tablename__ = "predictions"

    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(50), ForeignKey("customers.customer_id"), nullable=False)
    prediction = Column(String(20), nullable=False)
    probability = Column(Float, nullable=False)
    risk_level = Column(String(30), nullable=False)
    confidence_score = Column(Float, nullable=False)
    model_name = Column(String(100), nullable=False, default="Gradient Boosting Classifier")
    prediction_time = Column(DateTime, default=datetime.datetime.now)

    customer = relationship("Customer", back_populates="predictions")


class ModelInfo(Base):
    """SQLAlchemy ORM model for tracking trained model metadata and versions."""
    __tablename__ = "model_info"

    model_id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    algorithm = Column(String(100), nullable=False)
    accuracy = Column(Float, nullable=False)
    precision_score = Column(Float, nullable=False)
    recall_score = Column(Float, nullable=False)
    f1_score = Column(Float, nullable=False)
    roc_auc = Column(Float, nullable=False)
    training_date = Column(DateTime, default=datetime.datetime.now)
    version = Column(String(20), nullable=False, default="1.0.0")


class ApplicationLog(Base):
    """SQLAlchemy ORM model for tracking system execution and application logs."""
    __tablename__ = "application_logs"

    log_id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="SUCCESS")
    created_at = Column(DateTime, default=datetime.datetime.now)


def init_db():
    """Initializes and creates all database tables if they do not already exist."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database tables: {e}")
        raise e


if __name__ == "__main__":
    init_db()
    print("Database ORM tables created successfully.")
