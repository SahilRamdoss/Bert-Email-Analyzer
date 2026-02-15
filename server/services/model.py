from typing import List
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np

class Model:

    def __init__(self, model_path:str, device:str = "cuda"):
        self.device = device if torch.cuda.is_available() else "cpu"
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)

        # Put model in eval mode
        self.model.eval()


    def predict(self, emails: List[str]):

        input_ids = self.tokenizer(emails, max_length=512, truncation=True, padding=True, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**input_ids)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1).cpu().tolist()

        return predictions