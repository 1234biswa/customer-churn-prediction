import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.utils.logger import logger
from src.utils.exception import CustomException

@dataclass
class DataIngestionConfig:
    """
    Configuration dataclass for Data Ingestion component.
    Defines input raw dataset path and output train/test artifact paths.
    """
    raw_data_path: str = os.path.join("data", "raw", "Telco-Customer-Churn.csv")
    train_data_path: str = os.path.join("data", "processed", "train.csv")
    test_data_path: str = os.path.join("data", "processed", "test.csv")
    test_size: float = 0.2
    random_state: int = 42


class DataIngestion:
    """
    Data Ingestion component responsible for loading raw customer churn data,
    performing initial data inspection, and splitting data into train and test sets.
    """

    def __init__(self, config: DataIngestionConfig = DataIngestionConfig()):
        self.ingestion_config = config

    def initiate_data_ingestion(self) -> tuple[str, str]:
        """
        Loads dataset, logs shape, missing values, duplicate count, inspects data,
        and saves raw, train, and test CSV files.

        Returns:
            tuple[str, str]: Paths to the generated train.csv and test.csv files.
        """
        logger.info("Starting Data Ingestion component...")
        try:
            # 1. Verify and read raw CSV file
            if not os.path.exists(self.ingestion_config.raw_data_path):
                raise FileNotFoundError(
                    f"Raw dataset file not found at: {self.ingestion_config.raw_data_path}"
                )

            logger.info(f"Reading raw dataset from: {self.ingestion_config.raw_data_path}")
            df = pd.read_csv(self.ingestion_config.raw_data_path)

            # 2. Display basic metadata & observations
            logger.info("Dataset successfully loaded into DataFrame.")
            logger.info(f"Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns")

            # Check missing values
            null_counts = df.isnull().sum()
            total_nulls = null_counts.sum()
            logger.info(f"Total missing values across all columns: {total_nulls}")

            # Check duplicates
            duplicate_count = df.duplicated().sum()
            logger.info(f"Duplicate rows found: {duplicate_count}")

            # 3. Create destination directories if they don't exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # 4. Perform Train-Test Split (80% Train, 20% Test)
            logger.info(f"Splitting data into Train ({1 - self.ingestion_config.test_size:.0%}) and Test ({self.ingestion_config.test_size:.0%})...")
            train_set, test_set = train_test_split(
                df,
                test_size=self.ingestion_config.test_size,
                random_state=self.ingestion_config.random_state,
                stratify=df["Churn"] if "Churn" in df.columns else None
            )

            # 5. Save split files
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logger.info(f"Saved train dataset to: {self.ingestion_config.train_data_path} (Shape: {train_set.shape})")
            logger.info(f"Saved test dataset to: {self.ingestion_config.test_data_path} (Shape: {test_set.shape})")
            logger.info("Data Ingestion component completed successfully.")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            logger.error("Error encountered during Data Ingestion execution!")
            raise CustomException(e, sys)


if __name__ == "__main__":
    # Quick execution for testing Data Ingestion independently
    try:
        ingestion = DataIngestion()
        train_path, test_path = ingestion.initiate_data_ingestion()
        print(f"\nIngestion Successful!\nTrain Path: {train_path}\nTest Path: {test_path}")
    except Exception as e:
        print(f"Ingestion Failed: {e}")
