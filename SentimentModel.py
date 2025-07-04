import json
import os
from transformers import pipeline


class SentimentAnalyzerModel:
    def __init__(self, config_path=None):
        if config_path is None:
            # Domyślna ścieżka względem tego pliku
            config_path = os.path.join(os.path.dirname(__file__), "config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        model_name = config["model_name"]

        self.pipe = pipeline("text-classification", model=model_name)

    def analyze(self, text):
        result = self.pipe(text)
        label = result[0]['label']
        score = result[0]['score']
        return label, score
