import re
import os
import nltk
from collections import Counter
import json

# This clean_text function is a local copy from 01dataprep_clean_lemmatize.py
# PIPELINE RISK: If you change the function in 01, you MUST change it here too!
def clean_text(text: str) -> str:
    """Converts text to lowercase and removes punctuation and numbers."""
    text = text.lower()
    text = re.sub(r'[^а-я\s]', '', text)
    return text

def parse_text_file(file_path: str) -> str:
    """Reads a text file and returns its contents as a single string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"Reading {os.path.basename(file_path)}...")
            return file.read()
    except FileNotFoundError:
        print(f"ERROR: The file was not found at '{file_path}'")
        return ""

def create_syntactic_inputs(input_files: list):
    """
    Reads original text files, cleans them WITHOUT lemmatizing,
    and creates mfinder input files based on unlemmatized bigrams.
    """
    print("--- Starting Syntactic mfinder Input Generation ---")
    
    output_dir = "syntactic-analysis"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    for filename in input_files:
        print(f"\nProcessing {filename}...")
        book_name = filename.split('.txt')[0]
        
        # 1. Read the original file
        original_text = parse_text_file(filename)
        if not original_text:
            continue
            
        # 2. Clean the text (unlemmatized)
        cleaned_text = clean_text(original_text)
        
        # 3. Tokenize
        tokens = cleaned_text.split()
        if not tokens:
            print(f"No tokens found in {filename}. Skipping.")
            continue
            
        # 4. Get bigram frequencies
        bigram_freqs = Counter(nltk.ngrams(tokens, 2))
        
        # 5. Create vocabulary and word-to-ID mapping
        vocabulary = set(tokens)
        sorted_vocab = sorted(list(vocabulary))
        word_to_id = {word: i + 1 for i, word in enumerate(sorted_vocab)}

        # 6. Write the mfinder input file, SKIPPING self-edges
        output_input_path = os.path.join(output_dir, f"{book_name}_syntactic_input.txt")
        self_edge_count = 0
        with open(output_input_path, 'w', encoding='utf-8') as f:
            for (word1, word2), weight in bigram_freqs.items():
                
                # Skip self-loops
                if word1 == word2:
                    self_edge_count += 1
                    continue
                
                id1 = word_to_id[word1]
                id2 = word_to_id[word2]
                f.write(f"{id1} {id2} {weight}\n")
        
        print(f"Created syntactic input file: {output_input_path}")
        if self_edge_count > 0:
            print(f"   (Removed {self_edge_count} self-edges)")

        # 7. Save the corresponding mapping file
        output_mapping_path = os.path.join(output_dir, f"{book_name}_syntactic_mapping.json")
        with open(output_mapping_path, 'w', encoding='utf-8') as f:
            json.dump(word_to_id, f, ensure_ascii=False, indent=4)
            
        print(f"Saved syntactic word-to-ID map: {output_mapping_path}")

# --- Main processing loop ---
if __name__ == '__main__':
    input_files = ['Ru1.txt', 'Ru2.txt', 'Ru3.txt', 'Ru4.txt',Z', 'Ru5.txt']
    create_syntactic_inputs(input_files)
    print("\n--- All syntactic mfinder inputs created successfully! ---")