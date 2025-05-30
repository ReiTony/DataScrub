import pandas as pd
from app.services.data_cleaner import DataCleaner
from app.services.data_visualizer import DataVisualizer
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ChatEngine:
    def __init__(self, df: pd.DataFrame, output_dir: str):
        self.df = df
        self.output_dir = output_dir

    def handle_prompt(self, prompt: str) -> dict:
        prompt_lower = prompt.lower()
        logger.info(f"Received prompt: {prompt}")

        if "clean" in prompt_lower:
            cleaner = DataCleaner(self.df)
            cleaned_df, report = cleaner.clean()
            self.df = cleaned_df 
            return {
                "action": "cleaning",
                "report": report
            }

        elif "missing" in prompt_lower:
            missing = self.df.isnull().sum()
            missing_summary = missing[missing > 0].to_dict()
            return {
                "action": "missing_values",
                "missing_summary": missing_summary
            }

        elif "visualize" in prompt_lower or "plot" in prompt_lower:
            visualizer = DataVisualizer(self.df, self.output_dir)
            plot_paths = visualizer.visualize()
            return {
                "action": "visualization",
                "plots": plot_paths
            }

        elif "heatmap" in prompt_lower:
            visualizer = DataVisualizer(self.df, self.output_dir)
            visualizer.plot_correlation_heatmap()
            return {
                "action": "heatmap",
                "plots": [f"{self.output_dir}/correlation_heatmap.png"]
            }

        elif "summary" in prompt_lower or "describe" in prompt_lower:
            summary = self.df.describe(include="all").fillna("").to_dict()
            return {
                "action": "summary_stats",
                "summary": summary
            }

        else:
            return {
                "action": "unknown",
                "message": "Sorry, I didn't understand that. Try 'clean the dataset', 'show missing values', or 'visualize'."
            }
