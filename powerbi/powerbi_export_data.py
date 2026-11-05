import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
from src.db import SessionLocal, get_prediction_history
from src.utils.logger import logger

def export_powerbi_datasets():
    """
    Exports cleaned customer records and database predictions into Power BI ready CSV datasets.
    """
    try:
        os.makedirs("powerbi", exist_ok=True)
        logger.info("Exporting datasets for Power BI dashboard integration...")

        # 1. Cleaned Dataset Export
        cleaned_path = os.path.join("data", "processed", "cleaned_telco_customer_churn.csv")
        if os.path.exists(cleaned_path):
            df_cleaned = pd.read_csv(cleaned_path)
            # Add engineered features for Power BI slicing
            bins = [-1, 12, 24, 48, 60, 100]
            labels = ["0-12 Months", "12-24 Months", "24-48 Months", "48-60 Months", "60+ Months"]
            df_cleaned["TenureGroup"] = pd.cut(df_cleaned["tenure"], bins=bins, labels=labels)
            
            pbi_cleaned_path = os.path.join("powerbi", "powerbi_customer_churn_dataset.csv")
            df_cleaned.to_csv(pbi_cleaned_path, index=False)
            logger.info(f"Exported Power BI Customer Dataset to: {pbi_cleaned_path} (Rows: {len(df_cleaned)})")

        # 2. Database Predictions Log Export
        db = SessionLocal()
        try:
            history_df = get_prediction_history(db, limit=5000)
            if not history_df.empty:
                pbi_pred_path = os.path.join("powerbi", "powerbi_prediction_history.csv")
                history_df.to_csv(pbi_pred_path, index=False)
                logger.info(f"Exported Power BI Prediction History to: {pbi_pred_path} (Rows: {len(history_df)})")
        finally:
            db.close()

        logger.info("Power BI data export completed successfully.")

    except Exception as e:
        logger.error(f"Failed to export Power BI dataset: {e}")

if __name__ == "__main__":
    export_powerbi_datasets()
