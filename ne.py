# import pandas as pd
# import ast
# import shutil
# import numpy as np
# from transformers import BertTokenizerFast, BertForTokenClassification, Trainer, TrainingArguments
# from datasets import Dataset
# from seqeval.metrics import classification_report
# from sklearn.model_selection import train_test_split
# from dataclasses import dataclass
# from typing import Any, Dict, List
# from google.colab import files

# # Load the single dataset
# file_path = 'train.xlsx'  # Update with your actual file path
# data = pd.read_excel(file_path)

# # Convert 'assistant' column (JSON-like structure) to entity tags
# def extract_labels(text, entity_data):
#     words = text.split()
#     labels = ['O'] * len(words)

#     if isinstance(entity_data, str):  # Ensure it's parsed correctly
#         try:
#             entity_data = ast.literal_eval(entity_data)  # Convert string to dictionary
#         except Exception:
#             return words, labels

#     for entity, values in entity_data.items():
#         for value in values:
#             value_words = value.split()
#             for i in range(len(words) - len(value_words) + 1):
#                 if words[i:i+len(value_words)] == value_words:
#                     labels[i] = f'B-{entity}'
#                     for j in range(1, len(value_words)):
#                         labels[i+j] = f'I-{entity}'
#     return words, labels

# # Process dataset into word-label pairs
# sentences = []
# tags = []

# for _, row in data.iterrows():
#     words, labels = extract_labels(str(row['user']), str(row['assistant']))
#     sentences.append(words)
#     tags.append(labels)

# processed_data = pd.DataFrame({'Words': sentences, 'Tags': tags})

# # **Split dataset into 70% Train, 20% Validation, 10% Test**
# train_data, temp_data = train_test_split(processed_data, test_size=0.3, random_state=42)  
# validate_data, test_data = train_test_split(temp_data, test_size=1/3, random_state=42)

# # Convert lists to object dtype
# def convert_dtype(df):
#     return df.astype({'Words': 'object', 'Tags': 'object'})

# train_data = convert_dtype(train_data)
# validate_data = convert_dtype(validate_data)
# test_data = convert_dtype(test_data)

# # Save to Excel for verification
# train_data.to_excel('train_split.xlsx', index=False)
# validate_data.to_excel('validate_split.xlsx', index=False)
# test_data.to_excel('test_split.xlsx', index=False)

# # Generate tag mappings
# tag_list = sorted(list(set([tag for tags in train_data['Tags'] for tag in tags])))
# tag2id = {tag: i for i, tag in enumerate(tag_list)}
# id2tag = {i: tag for tag, i in tag2id.items()}

# print(tag_list)

# # Tokenization using FinBERT
# tokenizer = BertTokenizerFast.from_pretrained('ProsusAI/finbert')

# def tokenize_and_align_labels(examples):
#     tokenized_inputs = tokenizer(
#         examples['Words'],
#         truncation=True,
#         is_split_into_words=True,
#         padding='max_length',
#         max_length=128,
#         return_tensors=None
#     )

#     labels = []
#     for i, label in enumerate(examples['Tags']):
#         word_ids = tokenized_inputs.word_ids(batch_index=i)
#         previous_word_idx = None
#         label_ids = []

#         for word_idx in word_ids:
#             if word_idx is None:
#                 label_ids.append(-100)
#             elif word_idx != previous_word_idx:
#                 label_ids.append(tag2id[label[word_idx]])
#             else:
#                 label_ids.append(-100)
#             previous_word_idx = word_idx

#         labels.append(label_ids)

#     tokenized_inputs['labels'] = labels
#     return tokenized_inputs

# # Convert to Hugging Face datasets
# train_dataset = Dataset.from_pandas(train_data)
# test_dataset = Dataset.from_pandas(test_data)
# validate_dataset = Dataset.from_pandas(validate_data)

# tokenized_train_dataset = train_dataset.map(tokenize_and_align_labels, batched=True, remove_columns=train_dataset.column_names)
# tokenized_test_dataset = test_dataset.map(tokenize_and_align_labels, batched=True, remove_columns=test_dataset.column_names)
# tokenized_validate_dataset = validate_dataset.map(tokenize_and_align_labels, batched=True, remove_columns=validate_dataset.column_names)

# # Load FinBERT model
# model = BertForTokenClassification.from_pretrained(
#     'ProsusAI/finbert',
#     num_labels=len(tag_list)
# )

# @dataclass
# class DataCollatorForTokenClassification:
#     tokenizer: Any
#     padding: bool = True
#     max_length: int = 128
#     pad_to_multiple_of: int = None

#     def __call__(self, features: List[Dict[str, Any]]):
#         batch = {key: [feature[key] for feature in features] for key in features[0].keys()}
#         batch = self.tokenizer.pad(
#             batch,
#             padding=self.padding,
#             max_length=self.max_length,
#             pad_to_multiple_of=self.pad_to_multiple_of,
#             return_tensors='pt'
#         )
#         return batch

# # Training arguments
# training_args = TrainingArguments(
#     output_dir='./results',
#     eval_strategy='epoch',
#     learning_rate=3e-5,
#     per_device_train_batch_size=16,
#     per_device_eval_batch_size=16,
#     num_train_epochs=5,
#     weight_decay=0.01,
#     save_strategy='epoch',
#     logging_steps=100,
#     load_best_model_at_end=True,
#     metric_for_best_model='loss'
# )

# # Trainer setup
# trainer = Trainer(
#     model=model,
#     args=training_args,
#     train_dataset=tokenized_train_dataset,
#     eval_dataset=tokenized_validate_dataset,
#     data_collator=DataCollatorForTokenClassification(tokenizer)
# )

# # Train model
# trainer.train()

# # Save model
# tokenizer.save_pretrained("./ner_model_fin")
# model.save_pretrained("./ner_model_fin")

# # Zip the model directory
# shutil.make_archive("/content/ner_model_fin", 'zip', "/content/ner_model_fin")

# # Download the zipped model
# files.download("/content/ner_model_fin.zip")

# # Evaluation
# predictions, labels, _ = trainer.predict(tokenized_test_dataset)
# preds = predictions.argmax(-1)

# # Convert predictions to tags
# true_labels = [[id2tag[label] for label in example if label != -100] for example in labels]
# pred_labels = [[id2tag[pred] for (pred, label) in zip(pred_example, label_example) if label != -100]
#                for pred_example, label_example in zip(preds, labels)]

# print(classification_report(true_labels, pred_labels))
