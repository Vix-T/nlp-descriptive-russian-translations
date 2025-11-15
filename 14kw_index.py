import pandas as pd
import os
import math
import csv
from collections import Counter

def calculate_yules_k(tokens: list):
    """Calculates Yule's K measure of lexical diversity."""
    if not tokens:
        return 0
    
    N = len(tokens)
    token_counts = Counter(tokens)
    freq_of_freqs = Counter(token_counts.values())
    M1 = sum([(freq * freq) * count for freq, count in freq_of_freqs.items()])
    
    if N * N == 0:
        return 0
        
    K = 10000 * (M1 - N) / (N * N)
    return K

def calculate_honores_w(tokens: list):
    """Calculates Honoré's W measure of lexical richness."""
    if not tokens:
        return 0
    
    N = len(tokens) # Total number of words (tokens)
    token_counts = Counter(tokens)
    V = len(token_counts) # Number of unique words (types)
    
    # V1 is the number of words that appear only once (hapax legomena)
    V1 = sum(1 for count in token_counts.values() if count == 1)
    
    # Avoid division by zero if V is 0 or if all words are unique (V1=V)
    if V == 0 or V == V1:
        return 0
        
    W = 100 * (math.log(N) / (1 - (V1 / V)))
    return W

if __name__ == "__main__":
    output_csv_file = 'lexical_diversity_results.csv'
    header = ['Filename', 'Yules_K', 'Honores_W']
    
    # --- FIXED: Using the correct input files from our pipeline ---
    files_to_analyze = [f for f in os.listdir('.') if f.startswith('Ru') and f.endswith('_clean_lemmatized_nostops.txt')]
    
    if not files_to_analyze:
        print(f"ERROR: No '{files_to_analyze}' files found in this directory.")
    else:
        print(f"Found {len(files_to_analyze)} files. Starting analysis...")
        
        all_results = []
        for filename in sorted(files_to_analyze):
            print(f"--- Analyzing '{filename}' ---")
            with open(filename, 'r', encoding='utf-8') as text_file:
                tokens = text_file.read().split()
                
                yules_k = calculate_yules_k(tokens)
                honores_w = calculate_honores_w(tokens)
                
                print(f"  Yule's K: {yules_k:.4f}")
                print(f"  Honoré's W: {honores_w:.4f}\n")
                all_results.append([filename, yules_k, honores_w])
        
        # Write to CSV
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in all_results:
                writer.writerow(row)
        
        print(f"All analyses are complete. Results have been saved to '{output_csv_file}'")