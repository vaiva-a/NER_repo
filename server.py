from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizerFast, BertForTokenClassification
import torch

# Load Model and Tokenizer
model_path = r"D:/ner_model2"  # Adjust the path if necessary
model = BertForTokenClassification.from_pretrained(model_path)
tokenizer = BertTokenizerFast.from_pretrained(model_path)
model.eval()

# Tag Mapping
id2tag = {
    0: 'B-LOC', 1: 'B-MISC', 2: 'B-ORG', 3: 'B-PER',
    4: 'I-LOC', 5: 'I-MISC', 6: 'I-ORG', 7: 'I-PER',
    8: 'O', 9: 'nan'
}

# FastAPI App
app = FastAPI()

# Request Model
class ParagraphRequest(BaseModel):
    paragraph: str

@app.post("/predict")
def predict(request: ParagraphRequest):
    """Processes a paragraph and returns NER tags in allTagData format."""
    lines = request.paragraph.split(".")  # Split paragraph into lines
    allTagData = {}

    for index, line in enumerate(lines):
        words = line.strip().split()
        tokens = tokenizer(words, truncation=True, is_split_into_words=True, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**tokens)

        predictions = torch.argmax(outputs.logits, dim=-1).squeeze().tolist()
        word_ids = tokens.word_ids()

        tagData = {}
        previous_word_idx = None

        for word_idx, pred in zip(word_ids, predictions):
            if word_idx is not None and word_idx != previous_word_idx:
                tagData[word_idx] = {
                    "word": words[word_idx],
                    "tag": id2tag.get(pred, "O")
                }
            previous_word_idx = word_idx

        allTagData[index] = {
            "sentence_number": index,
            "annotations": tagData
        }

    return allTagData

# Root Route
@app.get("/")
def home():
    return {"message": "NER API is running"}
