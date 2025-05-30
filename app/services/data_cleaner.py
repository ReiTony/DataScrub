import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DataCleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.report = []

    def standardize_columns(self):
        self.df.columns = [
            col.strip().lower().replace(" ", "_") for col in self.df.columns
        ]
        step = "Standardized column names."
        self.report.append(step)
        logger.info(step)
        return self

    def drop_duplicates(self):
        initial = len(self.df)
        self.df.drop_duplicates(inplace=True)
        removed = initial - len(self.df)
        step = f"Removed {removed} duplicate rows."
        self.report.append(step)
        logger.info(step)
        return self

    def handle_nulls(self, strategy: str = "median"):
        null_summary = self.df.isnull().sum()
        total_filled = 0

        for col, nulls in null_summary.items():
            if nulls > 0:
                if self.df[col].dtype in ["int64", "float64"]:
                    fill_value = (
                        self.df[col].median()
                        if strategy == "median"
                        else self.df[col].mean()
                    )
                    self.df[col].fillna(fill_value, inplace=True)
                    step = f"Filled {nulls} nulls in '{col}' with {strategy} ({fill_value})."
                else:
                    self.df[col].fillna("Unknown", inplace=True)
                    step = f"Filled {nulls} nulls in '{col}' with 'Unknown'."
                self.report.append(step)
                logger.info(step)
                total_filled += nulls

        if total_filled == 0:
            step = "No null values found; no filling applied."
            self.report.append(step)
            logger.info(step)
        return self

    def handle_outliers(self, z_thresh: float = 3.0):
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        count = 0
        for col in num_cols:
            z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
            outliers = z_scores > z_thresh
            outlier_count = outliers.sum()
            count += outlier_count
            self.df = self.df[~outliers]
        step = f"Removed {count} outlier rows using z-score threshold of {z_thresh}."
        self.report.append(step)
        logger.info(step)
        return self

    def clean(
        self,
        drop_dupes: bool = True,
        handle_nulls: bool = True,
        handle_outliers: bool = True,
        null_strategy: str = "median",
        outlier_thresh: float = 3.0,
    ):
        self.standardize_columns()

        if drop_dupes:
            self.drop_duplicates()
        if handle_nulls:
            self.handle_nulls(strategy=null_strategy)
        if handle_outliers:
            self.handle_outliers(z_thresh=outlier_thresh)

        logger.info("Cleaning complete.")
        return self.df, self.report
