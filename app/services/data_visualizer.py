import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DataVisualizer:
    def __init__(self, df: pd.DataFrame, output_dir: str):
        self.df = df.copy()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.generated_plots = []

    def plot_histograms(self):
        numeric_cols = self.df.select_dtypes(include="number").columns
        for col in numeric_cols:
            plt.figure()
            self.df[col].hist(bins=20, color='skyblue', edgecolor='black')
            plt.title(f"Histogram of {col}")
            plt.xlabel(col)
            plt.ylabel("Frequency")
            plot_path = os.path.join(self.output_dir, f"{col}_hist.png")
            plt.savefig(plot_path)
            plt.close()
            self.generated_plots.append(plot_path)
            logger.info(f"Saved histogram: {plot_path}")
        return self

    def plot_correlation_heatmap(self):
        numeric_df = self.df.select_dtypes(include="number")
        if numeric_df.shape[1] < 2:
            logger.warning("Not enough numeric columns for heatmap.")
            return self

        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f", square=True)
        plt.title("Correlation Heatmap")
        plot_path = os.path.join(self.output_dir, "correlation_heatmap.png")
        plt.savefig(plot_path)
        plt.close()
        self.generated_plots.append(plot_path)
        logger.info(f"Saved correlation heatmap: {plot_path}")
        return self

    def plot_boxplots(self):
        numeric_cols = self.df.select_dtypes(include="number").columns
        for col in numeric_cols:
            plt.figure()
            sns.boxplot(x=self.df[col])
            plt.title(f"Boxplot of {col}")
            plot_path = os.path.join(self.output_dir, f"{col}_boxplot.png")
            plt.savefig(plot_path)
            plt.close()
            self.generated_plots.append(plot_path)
            logger.info(f"Saved boxplot: {plot_path}")
        return self

    def visualize(self, include_boxplots=True, include_histograms=True, include_heatmap=True):
        if include_histograms:
            self.plot_histograms()
        if include_heatmap:
            self.plot_correlation_heatmap()
        if include_boxplots:
            self.plot_boxplots()

        logger.info("Visualization complete.")
        return self.generated_plots