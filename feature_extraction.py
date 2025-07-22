import os
import re
import json
import math
from collections import Counter
import nltk
import pymorphy2

# --- Helper Functions ---

def read_tokens_from_file(file_path: str) -> list:
    """Reads a cleaned file and returns a list of tokens."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().split()
    except FileNotFoundError:
        print(f"❌ ERROR: File not found at '{file_path}'")
        return None

def sanitize_dict_for_json(obj):
    """
    Recursively sanitizes a dictionary or list to make it JSON-serializable.
    Converts Counter objects and tuple keys into JSON-safe formats.
    """
    if isinstance(obj, Counter):
        # If it's a Counter, convert its tuple keys to strings
        return {'_'.join(k): v for k, v in obj.items()}
    if isinstance(obj, dict):
        # If it's a dict, recurse on its values
        return {k: sanitize_dict_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        # If it's a list, recurse on its items
        return [sanitize_dict_for_json(item) for item in obj]
    if isinstance(obj, tuple):
        # If it's a tuple, convert it to a list
        return list(obj)
    # Return all other types as-is
    return obj

def save_features_to_json(features: dict, output_path: str):
    """Saves the extracted features dictionary to a JSON file."""
    try:
        # No custom encoder needed as the dictionary is already sanitized
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(features, f, ensure_ascii=False, indent=4)
        print(f"✅ Features successfully saved to {output_path}")
    except Exception as e:
        print(f"❌ ERROR saving JSON: {e}")

# --- Feature Extraction Functions (These are unchanged) ---

def get_ngram_freqs(tokens: list, n: int) -> Counter:
    if len(tokens) < n: return Counter()
    return Counter(nltk.ngrams(tokens, n))

def calculate_entropy(freq_dist: Counter, total_count: int) -> float:
    if not total_count: return 0
    entropy = -sum((count / total_count) * math.log2(count / total_count) for count in freq_dist.values())
    return entropy

def calculate_chunked_ttr(tokens: list, chunk_size: int = 2000) -> float:
    if not tokens: return 0
    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
    if len(chunks) > 1 and len(chunks[-1]) < chunk_size / 2: chunks.pop()
    if not chunks: return 0
    ttr_scores = [len(set(chunk)) / len(chunk) for chunk in chunks]
    return sum(ttr_scores) / len(ttr_scores)

def calculate_avg_sentence_length(original_file_path: str) -> float:
    try:
        with open(original_file_path, 'r', encoding='utf-8') as f: text = f.read()
        sentences = nltk.sent_tokenize(text, language='russian')
        if not sentences: return 0
        word_counts = [len(nltk.word_tokenize(sent, language='russian')) for sent in sentences]
        return sum(word_counts) / len(word_counts)
    except FileNotFoundError: return 0

def get_pos_freqs(tokens: list) -> Counter:
    morph = pymorphy2.MorphAnalyzer()
    pos_tags = [morph.parse(token)[0].tag.POS for token in tokens]
    return Counter(tag for tag in pos_tags if tag)

# --- Main Execution Block ---

if __name__ == "__main__":
    book_indices = range(1, 6)
    
    print("--- Starting Feature Extraction ---")

    for i in book_indices:
        book_name = f"Ru{i}"
        print(f"\n--- Processing {book_name} ---")
        book_features = {}

        # Part 1: Process '_clean.txt' files
        clean_file = f"{book_name}_clean.txt"
        tokens_with_stops = read_tokens_from_file(clean_file)
        if tokens_with_stops:
            print(f"Analyzing {clean_file}...")
            total_words = len(tokens_with_stops)
            unigram_freqs = get_ngram_freqs(tokens_with_stops, 1)
            bigram_freqs = get_ngram_freqs(tokens_with_stops, 2)
            book_features.update({
                'total_word_count': total_words,
                'unigram_frequencies': unigram_freqs,
                'bigram_frequencies': bigram_freqs,
                'trigram_frequencies': get_ngram_freqs(tokens_with_stops, 3),
                'unigram_entropy': calculate_entropy(unigram_freqs, total_words),
                'bigram_entropy': calculate_entropy(bigram_freqs, total_words - 1)
            })

        # Part 2: Process '_clean_nostops.txt' files
        nostops_file = f"{book_name}_clean_nostops.txt"
        tokens_no_stops = read_tokens_from_file(nostops_file)
        if tokens_no_stops:
            print(f"Analyzing {nostops_file}...")
            book_features.update({
                'content_word_count': len(tokens_no_stops),
                'unique_content_word_count': len(set(tokens_no_stops)),
                'mfw_frequencies': Counter(tokens_no_stops).most_common(100),
                'chunked_ttr': calculate_chunked_ttr(tokens_no_stops),
                'pos_frequencies': get_pos_freqs(tokens_no_stops)
            })

        # Part 3: Process original '.txt' file
        original_file = f"{book_name}.txt"
        print(f"Analyzing {original_file} for sentence structure...")
        book_features['avg_sentence_length'] = calculate_avg_sentence_length(original_file)

        # Sanitize the entire dictionary before saving
        sanitized_book_features = sanitize_dict_for_json(book_features)
        
        # Save the sanitized features to a single JSON file
        output_json_path = f"{book_name}_features.json"
        save_features_to_json(sanitized_book_features, output_json_path)
    
    print("\n--- All books processed. Feature extraction complete. ---")