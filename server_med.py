from fastapi import FastAPI, Body
from pydantic import BaseModel
from datasets import Dataset
from transformers import BertTokenizerFast, BertModel
from torch import nn
from torchcrf import CRF
from dataclasses import dataclass
from typing import List, Dict
import pandas as pd
import torch
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Define BioBERT CRF model architecture
class BertCRFNER(nn.Module):
    def __init__(self, bert_model_name, num_labels):
        super(BertCRFNER, self).__init__()
        self.bert = BertModel.from_pretrained(bert_model_name)
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)
        self.crf = CRF(num_labels, batch_first=True)

    def forward(self, input_ids, attention_mask=None, labels=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = self.dropout(outputs.last_hidden_state)
        emissions = self.classifier(sequence_output)

        if labels is not None:
            mask = labels != -100
            labels = torch.where(mask, labels, torch.zeros_like(labels))
            loss = -self.crf(emissions, labels, mask=mask, reduction='mean')
            return loss
        else:
            return self.crf.decode(emissions, mask=attention_mask.bool())

# Define label mappings
label2id = {'Anatomy': 0, 'Chemical/Drug': 1, 'Disease': 2, 'Genetics': 3, 'O': 4, 
            'Organism': 5, 'Organization': 6, 'Person': 7, 'Procedure': 8, 'Symptom': 9}
id2label = {v: k for k, v in label2id.items()}

# Load BioBERT CRF model
model_name = "dmis-lab/biobert-base-cased-v1.1"
model_weights_path = "../bert_crf_epoch3.pt"

# Initialize model and tokenizer
try:
    # Create the model with proper architecture
    logger.info(f"Loading base model from {model_name}...")
    model = BertCRFNER(model_name, len(label2id))
    
    # Then load your fine-tuned weights if they exist
    if os.path.exists(model_weights_path):
        logger.info(f"Loading fine-tuned weights from {model_weights_path}")
        model.load_state_dict(torch.load(model_weights_path, map_location=torch.device('cpu')))
    else:
        logger.warning(f"Fine-tuned weights file {model_weights_path} not found. Using base model only.")
    
    model.eval()
    
    # Initialize tokenizer from same model
    logger.info(f"Loading tokenizer from {model_name}...")
    tokenizer = BertTokenizerFast.from_pretrained(model_name)
    
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise e

# Use GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {device}")
model = model.to(device)

# Initialize FastAPI app
app = FastAPI()

# Request format
class ParagraphRequest(BaseModel):
    paragraph: str

@app.get("/")
def home():
    return {"message": "Medical NER API is running"}

@app.post("/predict")
def predict(request: ParagraphRequest):
    """NER prediction using BioBERT-CRF."""
    lines = request.paragraph.split(".")
    allTagData = {}

    for idx, line in enumerate(lines):
        words = line.strip().split()
        if not words:
            continue

        # Tokenize while tracking word mapping
        encoding = tokenizer(words, is_split_into_words=True, return_tensors="pt", 
                            padding=True, truncation=True)
        
        # Move to correct device
        inputs = {k: v.to(device) for k, v in encoding.items() if k in ["input_ids", "attention_mask"]}
        
        with torch.no_grad():
            predictions = model(**inputs)  # CRF returns list of lists
        
        # Map predictions back to words with proper BIO tagging
        word_ids = encoding.word_ids(batch_index=0)
        tagData = {}
        previous_word_idx = None
        previous_tag = None
        
        for token_idx, word_idx in enumerate(word_ids):
            if word_idx is not None and word_idx != previous_word_idx:
                if token_idx < len(predictions[0]):  # Ensure index is in range
                    pred_id = predictions[0][token_idx]
                    tag = id2label.get(pred_id, "O")
                    
                    # Apply proper BIO tagging
                    if tag == "O":
                        final_tag = "O"
                    else:
                        # Check if this is a new entity or continuation
                        if previous_word_idx is None or previous_tag != tag or previous_word_idx + 1 != word_idx:
                            # New entity
                            final_tag = f"B-{tag}"
                        else:
                            # Continuation of previous entity
                            final_tag = f"I-{tag}"
                    
                    tagData[word_idx] = {
                        "word": words[word_idx],
                        "tag": final_tag
                    }
                    
                    previous_word_idx = word_idx
                    previous_tag = tag

        allTagData[idx] = {
            "sentence_number": idx,
            "annotations": tagData
        }

    return allTagData

# Function to align labels with tokenized words for training
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples['Words'],
        is_split_into_words=True,
        padding='max_length',
        truncation=True,
        max_length=512
    )

    labels = []
    for i, word_list in enumerate(examples['Words']):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = []
        for word_id in word_ids:
            if word_id is None:
                label_ids.append(-100)
            else:
                try:
                    tag = examples['Tags'][i][word_id]
                    # Convert tag format (B-TAG, I-TAG) to simple tag format
                    if tag.startswith("B-") or tag.startswith("I-"):
                        tag = tag[2:]
                    label_ids.append(label2id.get(tag, label2id["O"]))
                except (IndexError, KeyError):
                    label_ids.append(-100)
        labels.append(label_ids)

    tokenized_inputs['labels'] = labels
    return tokenized_inputs

# Function to get updated sentences
def get_updated_sentences(ann, autotaglist):
    updated_sentences = []

    for ini_sentence, fin_sentence in zip(ann, autotaglist):
        annotations_ini = ini_sentence.get("annotations", {})
        annotations_fin = fin_sentence.get("annotations", {})

        modified = False
        words = []
        tags = []

        # Convert string keys to integers if needed
        annotations_ini = {int(k) if isinstance(k, str) and k.isdigit() else k: v 
                           for k, v in annotations_ini.items()}
        annotations_fin = {int(k) if isinstance(k, str) and k.isdigit() else k: v 
                           for k, v in annotations_fin.items()}

        # Sort keys to ensure proper word order
        sorted_keys = sorted([k for k in annotations_fin.keys() if isinstance(k, int)])
        
        for word_idx in sorted_keys:
            if word_idx not in annotations_fin:
                continue
                
            fin_info = annotations_fin[word_idx]
            ini_info = annotations_ini.get(word_idx, {"tag": "O"})
            
            # Handle both dictionary and string tag formats
            fin_tag = fin_info["tag"] if isinstance(fin_info, dict) else fin_info
            ini_tag = ini_info["tag"] if isinstance(ini_info, dict) else ini_info
            
            word = fin_info["word"] if isinstance(fin_info, dict) and "word" in fin_info else f"word_{word_idx}"
            
            if fin_tag != ini_tag:
                modified = True
                
            words.append(word)
            tags.append(fin_tag)

        if modified and words and tags:
            updated_sentences.append({"Words": words, "Tags": tags})

    return pd.DataFrame(updated_sentences)

@app.post("/learn")
async def update_model_with_incremental_data(ann: list = Body(...), autotaglist: list = Body(...)):
    try:
        # Prepare training data
        incremental_train_data = get_updated_sentences(ann, autotaglist)

        if incremental_train_data.empty:
            return {"message": "No updated data to train on."}

        logger.info(f"Training on {len(incremental_train_data)} updated sentences")
        
        # Create dataset and tokenize
        incremental_dataset = Dataset.from_pandas(incremental_train_data)
        tokenized_incremental_dataset = incremental_dataset.map(
            tokenize_and_align_labels, batched=True
        )

        # Set model to training mode
        model.train()
        
        # Create optimizer
        optimizer = torch.optim.AdamW(model.parameters(), lr=3e-5)
        
        # Simple training loop
        for epoch in range(3):
            total_loss = 0
            batch_size = 8
            
            # Create batches
            for i in range(0, len(tokenized_incremental_dataset), batch_size):
                batch = tokenized_incremental_dataset[i:min(i+batch_size, len(tokenized_incremental_dataset))]
                
                # Prepare inputs
                input_ids = torch.tensor([b['input_ids'] for b in batch]).to(device)
                attention_mask = torch.tensor([b['attention_mask'] for b in batch]).to(device)
                labels = torch.tensor([b['labels'] for b in batch]).to(device)
                
                # Forward pass
                optimizer.zero_grad()
                loss = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
                
                # Backward pass and optimize
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
                
            logger.info(f"Epoch {epoch+1}/3, Loss: {total_loss}")
        
        # Save model
        logger.info(f"Saving model to {model_weights_path}")
        torch.save(model.state_dict(), model_weights_path)
        model.eval()  # Set back to evaluation mode
        
        return {"message": "Model updated successfully."}
    except Exception as e:
        logger.error(f"Error during model update: {str(e)}")
        model.eval()  # Ensure model is back in eval mode even if there's an error
        return {"message": f"Model update failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server_med:app", host="0.0.0.0", port=8000, reload=True)