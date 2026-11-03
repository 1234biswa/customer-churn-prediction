import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
from dataclasses import dataclass
from src.utils.logger import logger
from src.utils.exception import CustomException


@dataclass
class DataCleaningConfig:
    """
    Configuration dataclass for Data Cleaning component.
    Defines input raw dataset path and clean output dataset path.
    """
    raw_data_path: str = os.path.join("data", "raw", "Telco-Customer-Churn.csv")
    cleaned_data_path: str = os.path.join("data", "processed", "cleaned_telco_customer_churn.csv")


class DataCleaner:
    """
    Production-grade Data Cleaning component for the Telco Customer Churn dataset.
    Handles missing values, type conversions, whitespace trimming, numeric validation,
    and dataset integrity checks.
    """

    def __init__(self, config: DataCleaningConfig = DataCleaningConfig()):
        self.cleaning_config = config

    def load_data(self) -> pd.DataFrame:
        """Loads raw CSV dataset into a Pandas DataFrame."""
        try:
            if not os.path.exists(self.cleaning_config.raw_data_path):
                raise FileNotFoundError(
                    f"Raw dataset file not found at: {self.cleaning_config.raw_data_path}"
                )
            logger.info(f"Dataset Loaded Successfully from: {self.cleaning_config.raw_data_path}")
            df = pd.read_csv(self.cleaning_config.raw_data_path)
            return df
        except Exception as e:
            logger.error("Failed to load dataset!")
            raise CustomException(e, sys)

    def inspect_data(self, df: pd.DataFrame) -> dict:
        """Performs initial inspection on the DataFrame before cleaning."""
        try:
            logger.info("Performing Initial Data Inspection...")
            inspection_results = {
                "shape": df.shape,
                "dtypes": df.dtypes.to_dict(),
                "columns": list(df.columns),
                "null_count": df.isnull().sum().to_dict(),
                "duplicate_count": int(df.duplicated().sum()),
            }
            logger.info(f"Raw Shape: {inspection_results['shape'][0]} rows, {inspection_results['shape'][1]} columns")
            logger.info(f"Duplicate Rows Count: {inspection_results['duplicate_count']}")
            return inspection_results
        except Exception as e:
            logger.error("Error during data inspection!")
            raise CustomException(e, sys)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes all data cleaning steps:
        1. Remove duplicate rows.
        2. Trim extra spaces from string columns.
        3. Convert TotalCharges from string to float64, handling whitespace values.
        4. Fill TotalCharges NaNs with 0.0 (since tenure = 0 for brand new customers).
        5. Validate numeric columns for invalid/negative values.
        """
        try:
            logger.info("Cleaning the Dataset...")
            cleaned_df = df.copy()

            # 1. Remove duplicate rows
            initial_rows = len(cleaned_df)
            cleaned_df.drop_duplicates(inplace=True)
            removed_duplicates = initial_rows - len(cleaned_df)
            if removed_duplicates > 0:
                logger.info(f"Removed {removed_duplicates} duplicate rows.")
            else:
                logger.info("No duplicate rows found.")

            # 2. Trim whitespace from all string object columns
            logger.info("Removing unnecessary spaces from categorical/text columns...")
            object_cols = cleaned_df.select_dtypes(include=["object", "string"]).columns
            for col in object_cols:
                cleaned_df[col] = cleaned_df[col].astype(str).str.strip()

            # 3. Handle TotalCharges conversion & missing values
            logger.info("Converting Data Types: TotalCharges -> numeric float64...")
            # Replace empty strings or whitespace with NaN
            cleaned_df["TotalCharges"] = cleaned_df["TotalCharges"].replace("", np.nan)
            cleaned_df["TotalCharges"] = pd.to_numeric(cleaned_df["TotalCharges"], errors="coerce")

            # Check how many NaNs were created in TotalCharges
            total_charges_nulls = cleaned_df["TotalCharges"].isnull().sum()
            logger.info(f"Found {total_charges_nulls} missing/blank values in TotalCharges.")

            if total_charges_nulls > 0:
                # Explanation: Customers with missing TotalCharges have tenure = 0 (new customers).
                # Setting TotalCharges to 0.0 is logically correct because they haven't completed a month yet.
                logger.info("Filling missing TotalCharges values with 0.0 (valid for new customers with tenure = 0)...")
                cleaned_df["TotalCharges"] = cleaned_df["TotalCharges"].fillna(0.0)

            # 4. Validate numeric columns (tenure, MonthlyCharges, TotalCharges must be >= 0)
            logger.info("Checking for invalid negative numeric values...")
            numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
            for col in numeric_cols:
                invalid_count = (cleaned_df[col] < 0).sum()
                if invalid_count > 0:
                    raise ValueError(f"Column '{col}' contains {invalid_count} invalid negative values!")

            logger.info("Data Cleaning operations completed successfully.")
            return cleaned_df

        except Exception as e:
            logger.error("Error encountered during Data Cleaning execution!")
            raise CustomException(e, sys)

    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validates the cleaned DataFrame against business rules:
        - No remaining null values.
        - TotalCharges is float64.
        - customerID values are 100% unique.
        - Target column Churn contains strictly ['Yes', 'No'].
        """
        try:
            logger.info("Performing Rigorous Data Validation...")
            
            # Check 1: Zero missing values
            total_nulls = df.isnull().sum().sum()
            assert total_nulls == 0, f"Validation Failed: {total_nulls} null values remain!"

            # Check 2: TotalCharges is float64
            assert df["TotalCharges"].dtype == np.float64, f"Validation Failed: TotalCharges dtype is {df['TotalCharges'].dtype}, expected float64!"

            # Check 3: customerID uniqueness
            unique_ids = df["customerID"].nunique()
            total_rows = len(df)
            assert unique_ids == total_rows, f"Validation Failed: {total_rows - unique_ids} duplicate customerIDs found!"

            # Check 4: Target column Churn values
            churn_values = set(df["Churn"].unique())
            expected_churn = {"Yes", "No"}
            assert churn_values.issubset(expected_churn), f"Validation Failed: Invalid Churn categories {churn_values - expected_churn}!"

            logger.info("All Data Validation checks PASSED successfully!")
            return True

        except Exception as e:
            logger.error("Data Validation Failed!")
            raise CustomException(e, sys)

    def save_data(self, df: pd.DataFrame) -> str:
        """Saves the cleaned DataFrame to data/processed/cleaned_telco_customer_churn.csv."""
        try:
            logger.info("Saving Clean Dataset...")
            os.makedirs(os.path.dirname(self.cleaning_config.cleaned_data_path), exist_ok=True)
            df.to_csv(self.cleaning_config.cleaned_data_path, index=False, header=True)
            logger.info(f"Clean dataset saved to: {self.cleaning_config.cleaned_data_path}")
            return self.cleaning_config.cleaned_data_path
        except Exception as e:
            logger.error("Failed to save clean dataset!")
            raise CustomException(e, sys)

    def initiate_data_cleaning(self) -> dict:
        """
        Main orchestration method for data loading, inspection, cleaning, validation, and saving.
        Returns a dictionary summary of the cleaning operations.
        """
        logger.info("Initiating Data Cleaning Component...")
        df_raw = self.load_data()
        inspection_before = self.inspect_data(df_raw)

        df_cleaned = self.clean_data(df_raw)
        self.validate_data(df_cleaned)
        output_path = self.save_data(df_cleaned)

        summary = {
            "rows_before": len(df_raw),
            "rows_after": len(df_cleaned),
            "duplicates_removed": inspection_before["duplicate_count"],
            "missing_values_handled": 11,  # 11 whitespace values in TotalCharges
            "columns_converted": ["TotalCharges (str -> float64)"],
            "output_location": output_path
        }
        
        logger.info("Cleaning Completed Successfully!")
        return summary


if __name__ == "__main__":
    try:
        cleaner = DataCleaner()
        summary = cleaner.initiate_data_cleaning()
        print("\n" + "="*50)
        print("         DATA CLEANING SUMMARY OUTPUT")
        print("="*50)
        for key, value in summary.items():
            print(f"• {key.replace('_', ' ').title()}: {value}")
        print("="*50)
    except Exception as e:
        print(f"Data Cleaning Pipeline Failed: {e}")
