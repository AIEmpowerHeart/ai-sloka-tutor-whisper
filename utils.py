
import json

def load_sloka_library(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_sloka_text(data, chapter, number):
    return data[chapter][number]

def simple_explanation(text):
    return f"This sloka discusses a deep spiritual message. In simple terms: {text[:150]}..."
