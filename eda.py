import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass

from src.utils.logger import logger
from src.utils.exception import CustomException

# Set modern Seaborn theme & style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10


@dataclass
class EDAConfig:
    """
    Configuration dataclass for EDA component.
    Defines input cleaned dataset path and output figures directory.
    """
    cleaned_data_path: str = os.path.join("data", "processed", "cleaned_telco_customer_churn.csv")
    figures_dir: str = os.path.join("reports", "figures")


class ExploratoryDataAnalysis:
    """
    Exploratory Data Analysis component for generating dataset statistics,
    visualizing distributions, calculating feature correlations, and identifying churn patterns.
    """

    def __init__(self, config: EDAConfig = EDAConfig()):
        self.config = config
        os.makedirs(self.config.figures_dir, exist_ok=True)

    def load_cleaned_data(self) -> pd.DataFrame:
        """Loads cleaned dataset from CSV."""
        try:
            if not os.path.exists(self.config.cleaned_data_path):
                raise FileNotFoundError(
                    f"Cleaned dataset not found at: {self.config.cleaned_data_path}"
                )
            logger.info(f"Loading cleaned dataset from: {self.config.cleaned_data_path}")
            df = pd.read_csv(self.config.cleaned_data_path)
            return df
        except Exception as e:
            logger.error("Failed to load cleaned dataset!")
            raise CustomException(e, sys)

    def analyze_target_variable(self, df: pd.DataFrame) -> dict:
        """
        Analyzes Churn target column distribution and generates count plot & pie chart.
        """
        try:
            logger.info("Analyzing Target Variable (Churn)...")
            churn_counts = df["Churn"].value_counts()
            total_customers = len(df)
            retained_count = churn_counts.get("No", 0)
            churned_count = churn_counts.get("Yes", 0)
            churn_pct = (churned_count / total_customers) * 100
            retention_pct = (retained_count / total_customers) * 100

            logger.info(f"Total Customers: {total_customers}")
            logger.info(f"Retained Customers: {retained_count} ({retention_pct:.2f}%)")
            logger.info(f"Churned Customers: {churned_count} ({churn_pct:.2f}%)")

            # Create Figure: Target Distribution
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))

            # Subplot 1: Bar Countplot
            sns.countplot(data=df, x="Churn", hue="Churn", palette=["#2ecc71", "#e74c3c"], legend=False, ax=axes[0])
            axes[0].set_title("Customer Churn Count", fontsize=14, fontweight="bold")
            axes[0].set_xlabel("Churn Status")
            axes[0].set_ylabel("Customer Count")
            for p in axes[0].patches:
                height = p.get_height()
                axes[0].annotate(f'{int(height)} ({height/total_customers:.1%})',
                                 (p.get_x() + p.get_width() / 2., height / 2),
                                 ha='center', va='center', fontsize=11, color='white', fontweight='bold')

            # Subplot 2: Pie Chart
            axes[1].pie(
                [retained_count, churned_count],
                labels=["Retained (No)", "Churned (Yes)"],
                autopct="%1.1f%%",
                startangle=140,
                colors=["#2ecc71", "#e74c3c"],
                explode=(0, 0.08),
                shadow=True
            )
            axes[1].set_title("Customer Churn Percentage", fontsize=14, fontweight="bold")

            plt.tight_layout()
            save_path = os.path.join(self.config.figures_dir, "01_target_churn_distribution.png")
            plt.savefig(save_path, dpi=300)
            plt.close()
            logger.info(f"Saved Target Chart to: {save_path}")

            return {
                "total": total_customers,
                "retained": retained_count,
                "churned": churned_count,
                "churn_pct": churn_pct,
                "retention_pct": retention_pct
            }
        except Exception as e:
            logger.error("Error during target variable analysis!")
            raise CustomException(e, sys)

    def analyze_numerical_features(self, df: pd.DataFrame) -> dict:
        """
        Analyzes numerical features (tenure, MonthlyCharges, TotalCharges)
        and plots histogram/KDE and boxplots.
        """
        try:
            logger.info("Analyzing Numerical Features (tenure, MonthlyCharges, TotalCharges)...")
            num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
            stats_summary = df[num_cols].describe().to_dict()

            fig, axes = plt.subplots(3, 2, figsize=(14, 12))

            for idx, col in enumerate(num_cols):
                # Histogram + KDE
                sns.histplot(data=df, x=col, hue="Churn", kde=True, palette=["#2ecc71", "#e74c3c"], element="step", ax=axes[idx, 0])
                axes[idx, 0].set_title(f"Distribution of {col} by Churn", fontweight="bold")

                # Box Plot
                sns.boxplot(data=df, x="Churn", y=col, hue="Churn", palette=["#2ecc71", "#e74c3c"], legend=False, ax=axes[idx, 1])
                axes[idx, 1].set_title(f"{col} Outlier & Range Analysis", fontweight="bold")

            plt.tight_layout()
            save_path = os.path.join(self.config.figures_dir, "02_numerical_distributions.png")
            plt.savefig(save_path, dpi=300)
            plt.close()
            logger.info(f"Saved Numerical Distributions Chart to: {save_path}")

            return stats_summary
        except Exception as e:
            logger.error("Error analyzing numerical features!")
            raise CustomException(e, sys)

    def analyze_categorical_features(self, df: pd.DataFrame):
        """
        Generates churn comparison count plots across contract types, payment methods,
        internet services, and demographic variables.
        """
        try:
            logger.info("Analyzing Categorical Features & Churn Relationships...")

            # 1. Contract vs Churn
            plt.figure(figsize=(10, 5))
            sns.countplot(data=df, x="Contract", hue="Churn", palette=["#2ecc71", "#e74c3c"])
            plt.title("Churn Rate by Contract Type", fontsize=14, fontweight="bold")
            plt.xlabel("Contract Duration")
            plt.ylabel("Number of Customers")
            plt.tight_layout()
            save_path1 = os.path.join(self.config.figures_dir, "03_churn_by_contract.png")
            plt.savefig(save_path1, dpi=300)
            plt.close()

            # 2. Internet Service vs Churn
            plt.figure(figsize=(10, 5))
            sns.countplot(data=df, x="InternetService", hue="Churn", palette=["#2ecc71", "#e74c3c"])
            plt.title("Churn Rate by Internet Service Type", fontsize=14, fontweight="bold")
            plt.xlabel("Internet Service")
            plt.ylabel("Number of Customers")
            plt.tight_layout()
            save_path2 = os.path.join(self.config.figures_dir, "04_churn_by_internet_service.png")
            plt.savefig(save_path2, dpi=300)
            plt.close()

            # 3. Payment Method vs Churn
            plt.figure(figsize=(12, 5))
            sns.countplot(data=df, x="PaymentMethod", hue="Churn", palette=["#2ecc71", "#e74c3c"])
            plt.title("Churn Rate by Payment Method", fontsize=14, fontweight="bold")
            plt.xlabel("Payment Method")
            plt.ylabel("Number of Customers")
            plt.xticks(rotation=15)
            plt.tight_layout()
            save_path3 = os.path.join(self.config.figures_dir, "05_churn_by_payment_method.png")
            plt.savefig(save_path3, dpi=300)
            plt.close()

            # 4. Demographics (SeniorCitizen, Gender, Partner, Dependents)
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            sns.countplot(data=df, x="SeniorCitizen", hue="Churn", palette=["#2ecc71", "#e74c3c"], ax=axes[0, 0])
            axes[0, 0].set_title("Churn by Senior Citizen Status", fontweight="bold")
            axes[0, 0].set_xticks([0, 1])
            axes[0, 0].set_xticklabels(["Non-Senior (0)", "Senior (1)"])

            sns.countplot(data=df, x="gender", hue="Churn", palette=["#2ecc71", "#e74c3c"], ax=axes[0, 1])
            axes[0, 1].set_title("Churn by Gender", fontweight="bold")

            sns.countplot(data=df, x="Partner", hue="Churn", palette=["#2ecc71", "#e74c3c"], ax=axes[1, 0])
            axes[1, 0].set_title("Churn by Partner Status", fontweight="bold")

            sns.countplot(data=df, x="Dependents", hue="Churn", palette=["#2ecc71", "#e74c3c"], ax=axes[1, 1])
            axes[1, 1].set_title("Churn by Dependents Status", fontweight="bold")

            plt.tight_layout()
            save_path4 = os.path.join(self.config.figures_dir, "06_churn_by_demographics.png")
            plt.savefig(save_path4, dpi=300)
            plt.close()

            # 5. Tech Support & Online Security Add-ons
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            sns.countplot(data=df, x="TechSupport", hue="Churn", palette=["#2ecc71", "#e74c3c"], ax=axes[0])
            axes[0].set_title("Churn by Tech Support Add-on", fontweight="bold")

            sns.countplot(data=df, x="OnlineSecurity", hue="Churn", palette=["#2ecc71", "#e74c3c"], ax=axes[1])
            axes[1].set_title("Churn by Online Security Add-on", fontweight="bold")

            plt.tight_layout()
            save_path5 = os.path.join(self.config.figures_dir, "07_churn_by_tech_security.png")
            plt.savefig(save_path5, dpi=300)
            plt.close()

            logger.info("Categorical churn plots successfully generated.")
        except Exception as e:
            logger.error("Error analyzing categorical features!")
            raise CustomException(e, sys)

    def analyze_correlation_matrix(self, df: pd.DataFrame):
        """
        Computes numeric correlation matrix and saves heatmap.
        """
        try:
            logger.info("Calculating Feature Correlation Matrix...")
            df_encoded = df.copy()
            df_encoded["Churn_Binary"] = df_encoded["Churn"].map({"Yes": 1, "No": 0})
            
            num_cols = ["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "Churn_Binary"]
            corr_matrix = df_encoded[num_cols].corr()

            plt.figure(figsize=(8, 6))
            sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, cbar=True)
            plt.title("Correlation Matrix (Numerical Features & Target)", fontsize=14, fontweight="bold")
            plt.tight_layout()
            
            save_path = os.path.join(self.config.figures_dir, "08_correlation_heatmap.png")
            plt.savefig(save_path, dpi=300)
            plt.close()

            logger.info(f"Correlation Heatmap saved to: {save_path}")
            return corr_matrix.to_dict()
        except Exception as e:
            logger.error("Error computing correlation matrix!")
            raise CustomException(e, sys)

    def initiate_eda(self) -> dict:
        """Runs full EDA workflow and returns dataset summary statistics."""
        logger.info("Initiating Exploratory Data Analysis Pipeline...")
        df = self.load_cleaned_data()
        
        target_summary = self.analyze_target_variable(df)
        num_summary = self.analyze_numerical_features(df)
        self.analyze_categorical_features(df)
        corr_summary = self.analyze_correlation_matrix(df)

        logger.info("Exploratory Data Analysis Completed Successfully!")
        return {
            "target_summary": target_summary,
            "num_summary": num_summary,
            "corr_summary": corr_summary
        }


if __name__ == "__main__":
    try:
        eda = ExploratoryDataAnalysis()
        summary = eda.initiate_eda()
        print("\n" + "="*50)
        print("         EDA EXECUTION SUMMARY")
        print("="*50)
        print(f"• Total Customers: {summary['target_summary']['total']}")
        print(f"• Retained Count:  {summary['target_summary']['retained']} ({summary['target_summary']['retention_pct']:.2f}%)")
        print(f"• Churned Count:   {summary['target_summary']['churned']} ({summary['target_summary']['churn_pct']:.2f}%)")
        print("="*50)
    except Exception as e:
        print(f"EDA Execution Failed: {e}")
