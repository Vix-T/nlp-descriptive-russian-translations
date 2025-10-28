import math
import numpy as np
import nltk
from collections import Counter
import os
import csv

# --- Helper Functions for Calculations (Unchanged) ---

def calculate_ttr(tokens: list) -> float:
    if not tokens: return 0
    return len(set(tokens)) / len(tokens)

def calculate_unigram_entropy(tokens: list) -> float:
    if not tokens: return 0
    token_counts = Counter(tokens)
    total_tokens = len(tokens)
    entropy = 0.0
    for count in token_counts.values():
        probability = count / total_tokens
        entropy -= probability * math.log2(probability)
    return entropy

def calculate_bigram_entropy(tokens: list) -> float:
    if len(tokens) < 2: return 0
    bigrams = list(nltk.ngrams(tokens, 2))
    bigram_counts = Counter(bigrams)
    total_bigrams = len(bigrams)
    entropy = 0.0
    for count in bigram_counts.values():
        probability = count / total_bigrams
        entropy -= probability * math.log2(probability)
    return entropy
    
def calculate_conditional_entropy(tokens: list) -> float:
    if len(tokens) < 2: return 0
    unigram_counts = Counter(tokens)
    bigrams = list(nltk.ngrams(tokens, 2))
    bigram_counts = Counter(bigrams)
    total_unigrams = len(tokens)
    conditional_entropy = 0.0
    for bigram, bigram_count in bigram_counts.items():
        first_word = bigram[0]
        p_xy = bigram_count / total_unigrams
        p_x = unigram_counts[first_word] / total_unigrams
        if p_x > 0 and p_xy > 0:
            conditional_entropy -= p_xy * math.log2(p_xy / p_x)
    return conditional_entropy

# --- Main Analysis Function (Now returns results) ---

def run_text_analysis(filepath: str, chunk_size: int = 2000):
    print(f"--- Running Analysis on '{filepath}'...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            tokens = f.read().split()
    except FileNotFoundError:
        print(f"❌ ERROR: File not found at '{filepath}'.")
        return None

    chunks = [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
    if len(chunks) > 1 and len(chunks[-1]) < chunk_size / 2:
        chunks.pop()
    if not chunks:
        print(f"❌ ERROR: Not enough text in '{filepath}' to form a complete chunk.")
        return None

    print(f"Analyzing {len(chunks)} chunks of text...")

    ttr_scores = [calculate_ttr(chunk) for chunk in chunks]
    unigram_scores = [calculate_unigram_entropy(chunk) for chunk in chunks]
    bigram_scores = [calculate_bigram_entropy(chunk) for chunk in chunks]
    conditional_scores = [calculate_conditional_entropy(chunk) for chunk in chunks]
        
    # Return a dictionary of the calculated averages and standard deviations
    results = {
        "Avg_TTR": np.mean(ttr_scores), "Std_Dev_TTR": np.std(ttr_scores),
        "Avg_Unigram_Entropy": np.mean(unigram_scores), "Std_Dev_Unigram_Entropy": np.std(unigram_scores),
        "Avg_Bigram_Entropy": np.mean(bigram_scores), "Std_Dev_Bigram_Entropy": np.std(bigram_scores),
        "Avg_Conditional_Entropy": np.mean(conditional_scores), "Std_Dev_Conditional_Entropy": np.std(conditional_scores)
    }
    print("--- Analysis Complete ---\n")
    return results

# --- Main Execution Block (Now writes to a CSV file) ---
if __name__ == "__main__":
    output_csv_file = 'entropy_analysis_results.csv'
    header = [
        'Filename', 'Avg_TTR', 'Std_Dev_TTR', 
        'Avg_Unigram_Entropy', 'Std_Dev_Unigram_Entropy',
        'Avg_Bigram_Entropy', 'Std_Dev_Bigram_Entropy',
        'Avg_Conditional_Entropy', 'Std_Dev_Conditional_Entropy'
    ]

    files_to_analyze = [f for f in os.listdir('.') if f.startswith('Ru') and f.endswith('_clean.txt')]
    
    if not files_to_analyze:
        print("❌ No 'Ru#_clean.txt' files found in this directory.")
    else:
        print(f"Found {len(files_to_analyze)} files. Starting analysis...")
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header) # Write the header row
            
            for filename in sorted(files_to_analyze):
                analysis_results = run_text_analysis(filename)
                if analysis_results:
                    # Write the results for this file as a new row
                    row = [
                        filename,
                        f"{analysis_results['Avg_TTR']:.4f}", f"{analysis_results['Std_Dev_TTR']:.4f}",
                        f"{analysis_results['Avg_Unigram_Entropy']:.4f}", f"{analysis_results['Std_Dev_Unigram_Entropy']:.4f}",
                        f"{analysis_results['Avg_Bigram_Entropy']:.4f}", f"{analysis_results['Std_Dev_Bigram_Entropy']:.4f}",
                        f"{analysis_results['Avg_Conditional_Entropy']:.4f}", f"{analysis_results['Std_Dev_Conditional_Entropy']:.4f}"
                    ]
                    writer.writerow(row)
        
        print(f"\n✅ All analyses are complete. Results have been saved to '{output_csv_file}'")