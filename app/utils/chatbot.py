import os
import json
import logging
from huggingface_hub import InferenceClient
from decouple import config

HF_TOKEN = config("HUGGING_FACE_API")
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_user_intent(prompt: str) -> dict:
    system_instruction = (
        "You are a helpful assistant for a data cleaning and visualization API.\n"
        "Extract a JSON object from the user's request.\n"
        "Supported actions are: 'clean', 'visualize'.\n"
        "Optional flags include:\n"
        "- standardize (bool)\n"
        "- drop_duplicates (bool)\n"
        "- handle_nulls (bool)\n"
        "- handle_outliers (bool)\n"
        "- histograms (bool)\n"
        "- boxplots (bool)\n"
        "- heatmap (bool)\n"
        "Return only the JSON object."
    )

    full_prompt = f"<s>[INST] {system_instruction}\nUser: {prompt} [/INST]"
    logger.info(f"Sending prompt to LLM:\n{full_prompt}")

    try:
        response = client.text_generation(full_prompt, max_new_tokens=200, temperature=0.3)
        logger.info(f"Raw LLM response: {response}")

        # Find the first JSON object in the response
        json_start = response.find("{")
        json_end = response.rfind("}") + 1
        json_str = response[json_start:json_end]

        intent = json.loads(json_str)
        logger.info(f"Parsed intent: {intent}")
        return intent

    except Exception as e:
        logger.error(f"Failed to parse intent: {e}")
        return {"action": "unknown"}
