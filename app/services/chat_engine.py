import pandas as pd
import logging

from app.services.data_cleaner import DataCleaner
from app.services.data_visualizer import DataVisualizer
from app.utils.chatbot import parse_user_intent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ChatEngine:
    def __init__(self, df: pd.DataFrame, output_dir: str):
        self.df = df
        self.output_dir = output_dir

def handle_prompt(self, prompt: str) -> dict:
    logger.info(f"Received prompt: {prompt}")

    intent = parse_user_intent(prompt)
    action = intent.get("action")

    if action == "clean":
        cleaner = DataCleaner(self.df)
        if intent.get("standardize", True):
            cleaner.standardize_columns()
        if intent.get("drop_duplicates", True):
            cleaner.drop_duplicates()
        if intent.get("handle_nulls", True):
            cleaner.handle_nulls()
        if intent.get("handle_outliers", True):
            cleaner.handle_outliers()
        self.df, report = cleaner.df, cleaner.report
        return {"action": "cleaning", "report": report}

    elif action == "visualize":
        visualizer = DataVisualizer(self.df, self.output_dir)
        if intent.get("histograms", True):
            visualizer.plot_histograms()
        if intent.get("heatmap", False):
            visualizer.plot_correlation_heatmap()
        if intent.get("boxplots", False):
            visualizer.plot_boxplots()
        return {"action": "visualization", "plots": visualizer.generated_plots}

    elif action == "summary":
        summary = self.df.describe(include="all").fillna("").to_dict()
        return {"action": "summary_stats", "summary": summary}

    elif action == "missing_values":
        missing = self.df.isnull().sum()
        missing_summary = missing[missing > 0].to_dict()
        return {"action": "missing_values", "missing_summary": missing_summary}

    else:
        return {
            "action": "unknown",
            "message": "Sorry, I didn’t understand that. Try something like 'clean the dataset' or 'visualize heatmap only'."
        }
