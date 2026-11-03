import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utils.logger import logger
from src.utils.exception import CustomException

# Load environment variables from .env if present
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "customer_churn_db")


def get_db_engine():
    """
    Attempts to establish a MySQL connection using environment variables.
    If MySQL server is offline/unavailable, gracefully falls back to a local SQLite database engine.
    """
    mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    sqlite_url = "sqlite:///data/customer_churn_db.sqlite"

    try:
        # Try MySQL connection
        engine = create_engine(mysql_url, pool_pre_ping=True, connect_args={"connect_timeout": 2})
        with engine.connect() as conn:
            logger.info("Successfully connected to MySQL database engine!")
            return engine
    except Exception:
        logger.warning(
            f"MySQL connection to '{DB_NAME}' unavailable. Falling back to local SQLite database at 'data/customer_churn_db.sqlite'."
        )
        os.makedirs("data", exist_ok=True)
        engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
        return engine


# Create global Engine and SessionLocal factory
engine = get_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Context manager / dependency helper for retrieving database sessions."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
