import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
from src.utils.logger import logger
from src.utils.exception import CustomException


class FeatureEngineer:
    """
    Feature Engineering component responsible for deriving domain-specific
    features from customer demographic, service, and billing attributes.
    """

    def __init__(self):
        pass

    def transform_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates new engineered features:
        1. TenureGroup: Bins continuous tenure into 5 customer lifecycle stages.
        2. ChargesPerTenure: Calculates average monthly spend ratio across tenure.
        3. HasAddons: Counts active security and support add-ons.
        """
        try:
            logger.info("Applying Feature Engineering transformations...")
            df_fe = df.copy()

            # 1. Tenure Group Binned Categorical Feature
            # Lifecycle stages: <1 year (high churn), 1-2 years, 2-4 years, 4-5 years, 5+ years (loyalists)
            bins = [-1, 12, 24, 48, 60, 100]
            labels = ["0-12_Months", "12-24_Months", "24-48_Months", "48-60_Months", "60+_Months"]
            df_fe["TenureGroup"] = pd.cut(df_fe["tenure"], bins=bins, labels=labels)
            logger.info("Created feature: 'TenureGroup'")

            # 2. Charges Per Tenure Ratio
            # Avoid division by zero by adding 1 to tenure
            df_fe["ChargesPerTenure"] = df_fe["TotalCharges"] / (df_fe["tenure"] + 1)
            logger.info("Created feature: 'ChargesPerTenure'")

            # 3. Security & Support Add-on Count
            addon_cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport"]
            addon_count = (df_fe[addon_cols] == "Yes").sum(axis=1)
            df_fe["HasAddons"] = addon_count
            logger.info("Created feature: 'HasAddons'")

            logger.info(f"Feature Engineering completed. Total features: {df_fe.shape[1]}")
            return df_fe

        except Exception as e:
            logger.error("Error during Feature Engineering transformation!")
            raise CustomException(e, sys)
