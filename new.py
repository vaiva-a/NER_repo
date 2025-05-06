import pandas as pd
import random
import nltk
from nltk.corpus import wordnet
from collections import defaultdict
import itertools
from itertools import chain

nltk.download('wordnet')
nltk.download('omw-1.4')

# --- 1. Load Data ---
# Assume your data is in a CSV or Excel with columns: ID, Sentence_Number, Word, BIO_Tag
df = pd.read_excel('final_train_fix3.xlsx')  # <-- Change to your file name

# --- 2. Group by Sentences ---
def group_sentences(df):
    sentences = []
    grouped = df.groupby(['ID', 'Sentence_Number'])
    for (id_val, sent_num), group in grouped:
        words = group['Word'].tolist()
        tags = group['BIO_Tag'].tolist()
        sentences.append((id_val, sent_num, words, tags))
    return sentences

sentences = group_sentences(df)

# --- 3. Outlier Cleaning ---
def clean_sentence(words, tags):
    clean_words = []
    clean_tags = []
    for word, tag in zip(words, tags):
        # Ensure the word is a string before checking its length
        if isinstance(word, str):
            # Basic cleaning rule: if O-tagged and looks gibberish, drop or fix
            if len(word) > 30:  # suspiciously long word
                continue
            if tag.startswith('B-') or tag.startswith('I-'):
                clean_words.append(word)
                clean_tags.append(tag)
            else:
                # For O-words, accept as is
                clean_words.append(word)
                clean_tags.append(tag)
        else:
            # Handle non-string values (e.g., NaN or other types)
            continue
    return clean_words, clean_tags

cleaned_sentences = [clean_sentence(w, t) for (_, _, w, t) in sentences]

# --- 4. Synonym Replacement (O-tagged words only) ---
def synonym_replace(word):
    synonyms = wordnet.synsets(word)
    if synonyms:
        lemmas = set(chain.from_iterable([w.lemma_names() for w in synonyms]))
        lemmas.discard(word)  # don't include original word
        if lemmas:
            return random.choice(list(lemmas)).replace('_', ' ')
    return word  # if no synonyms, return original

def augment_synonyms(words, tags):
    new_words = []
    for word, tag in zip(words, tags):
        if tag == 'O' and random.random() < 0.3:  # 30% chance of replacing O-word
            new_words.append(synonym_replace(word.lower()))
        else:
            new_words.append(word)
    return new_words, tags

# --- 5. Entity Swapping ---
ENTITY_DICT = {
    'Military Families': 'Veteran Communities',
    'Child Adjustment': 'Youth Adaptation',
    # Add more entity replacements as needed
}

def swap_entities(words, tags):
    phrase = ' '.join(words)
    for original, replacement in ENTITY_DICT.items():
        if original in phrase:
            phrase = phrase.replace(original, replacement)
    new_words = phrase.split()
    # Assume same tag pattern; simple assumption for now
    return new_words, tags[:len(new_words)]

# --- 6. Reordering ---
def reorder_sentence(words, tags):
    if not words or not tags:  # Check if words or tags are empty
        return words, tags  # Return as is if empty
    chunks = list(zip(words, tags))
    random.shuffle(chunks)
    reordered_words, reordered_tags = zip(*chunks)
    return list(reordered_words), list(reordered_tags)


# --- 7. Generate Augmented Sentences ---
augmented_sentences = []

for (id_val, sent_num, words, tags) in sentences:
    words, tags = clean_sentence(words, tags)
    # Original
    augmented_sentences.append((id_val, sent_num, words, tags))
    
    for i in range(2):  # 2 augmentations per sentence
        choice = random.choice(['synonym', 'swap', 'reorder'])
        if choice == 'synonym':
            new_words, new_tags = augment_synonyms(words, tags)
        elif choice == 'swap':
            new_words, new_tags = swap_entities(words, tags)
        else:
            new_words, new_tags = reorder_sentence(words, tags)
        
        augmented_sentences.append((id_val, f"{sent_num}_aug{i+1}", new_words, new_tags))

# --- 8. Flatten back into Word-level format ---
records = []
for id_val, sent_num, words, tags in augmented_sentences:
    for word, tag in zip(words, tags):
        records.append({
            'ID': id_val,
            'Sentence_Number': sent_num,
            'Word': word,
            'BIO_Tag': tag
        })

final_df = pd.DataFrame(records)

# --- 9. Save to Excel ---
import numpy as np
import os

# Define the maximum number of rows per Excel file
MAX_EXCEL_ROWS = 1048570
chunk_size = MAX_EXCEL_ROWS

# Calculate the number of chunks needed
num_chunks = len(final_df) // chunk_size + (1 if len(final_df) % chunk_size != 0 else 0)

# Directory to save files
output_dir = "/content/augmented_ner_dataset_files"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# If data fits in one file, save normally
if num_chunks == 1:
    try:
        final_df.to_excel(f'{output_dir}/augmented_ner_dataset.xlsx', index=False)
        print("✅ Augmentation and Cleaning Complete! File saved as 'augmented_ner_dataset.xlsx'")
    except ValueError:
        # Fallback to CSV if Excel fails
        final_df.to_csv(f'{output_dir}/augmented_ner_dataset.csv', index=False)
        print("⚠️ Dataset too large for Excel. Saved as CSV instead: 'augmented_ner_dataset.csv'")
else:
    # If data is too large, split into multiple files
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(final_df))
        chunk = final_df.iloc[start_idx:end_idx]
        
        # Double-check we're not exceeding row limit
        if len(chunk) > MAX_EXCEL_ROWS:
            # Fallback to CSV for this chunk
            file_name = f'augmented_ner_dataset_part_{i+1}.csv'
            chunk.to_csv(f'{output_dir}/{file_name}', index=False)
            print(f"⚠️ Chunk {i+1} too large for Excel. Saved as CSV: {file_name}")
        else:
            # Save as Excel
            file_name = f'augmented_ner_dataset_part_{i+1}.xlsx'
            chunk.to_excel(f'{output_dir}/{file_name}', index=False)
            print(f"✅ Saved part {i+1} as {file_name}")
    
    print(f"✅ Augmentation and Cleaning Complete! Data split into {num_chunks} files.")

