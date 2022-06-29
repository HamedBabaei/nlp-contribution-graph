
from transformers import pipeline

class SummarizerInference:

    def __init__(self, model_path):
        self.summarizer = pipeline("summarization", model=model_path, tokenizer=model_path)
        pass

    def summarize(self, text):
        summary = self.summarizer(text, min_length=1, max_length=min(10, len(text)))
        return summary[0]['summary_text']
