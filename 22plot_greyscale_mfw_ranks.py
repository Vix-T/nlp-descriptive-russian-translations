#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a greyscale heatmap of the *ranks* of the most frequent
content words for a stylometry project.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
from collections import Counter

def load_tokens_from_file(filepath: pathlib.Path) -> list:
    """Loads a cleaned text file and returns a list of tokens."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().split()
    except FileNotFoundError:
        print(f"ERROR: File not found at {filepath}")
        return []
    except Exception as e:
        print(f"ERROR: Failed to parse {filepath}. Reason: {e}")
        return []

def main():
    # --- 1. Define Data and File Locations ---
    
    # This script reads from the MAIN directory, not 'conceptual-analysis'
    data_folder = pathlib.Path('.') 
    
    # Input: The "Content Only" files from Phase 1
    filenames = {
        'Ru-1911-Engelgardt': 'Ru1_clean_lemmatized_nostops.txt',
        'Ru-1926-Anon': 'Ru2_clean_lemmatized_nostops.txt',
        'Ru-1933-Chukovsky-(Ed.)': 'Ru3_clean_lemmatized_nostops.txt',
        'Ru-1949-Braude': 'Ru4_clean_lemmatized_nostops.txt',
        'Ru-1960-Daruzes': 'Ru5_clean_lemmatized_nostops.txt'
    }
    
    # --- 2. Calculate Frequencies ---
    print("--- Calculating word frequencies... ---")
    
    all_tokens = []
    book_freqs = {}
    
    for translator, filename in filenames.items():
        file_path = data_folder / filename
        tokens = load_tokens_from_file(file_path)
        
        if not tokens:
            continue
            
        book_freqs[translator] = Counter(tokens)
        all_tokens.extend(tokens)

    if not all_tokens:
        print("ERROR: No tokens were loaded. Halting.")
        return

    # --- 3. Find Top 30 Overall Content Words ---
    
    overall_freq = Counter(all_tokens)
    top_30_words = [word for word, count in overall_freq.most_common(30)]

    # --- 4. Build the Rank DataFrame ---
    print("--- Building Rank DataFrame... ---")
    
    df_freq = pd.DataFrame(columns=top_30_words, index=list(filenames.keys()))
    
    for translator, freqs in book_freqs.items():
        for word in top_30_words:
            df_freq.loc[translator, word] = freqs.get(word, 0)

    # Convert frequencies to ranks (1 = Most Frequent)
    df_ranks = df_freq.rank(axis=1, ascending=False, method="min")
    
    # --- 5. Draw the Heatmap ---
    print("--- Generating heatmap... ---")

    plt.figure(figsize=(20, 8))
    
    sns.heatmap(
        df_ranks,
        cmap="Greys",       
        annot=True,         # Show the rank number
        fmt=".0f",          # Format as integer
        linewidths=.5,
        cbar_kws={'label': 'Frequency Rank (1 = Most Frequent)'}
    )

    # --- 6. Customize Plot Labels ---
    
    plt.title('Relative Rank of Most Frequent Content Words', fontsize=16, pad=20)
    plt.ylabel('Translation', fontsize=12)
    plt.xlabel('Top 30 Content Words Over All Translations', fontsize=12)
    plt.yticks(rotation=0)
    plt.xticks(rotation=45, ha='right') 

    # --- 7. Save and Show ---
    
    output_file = 'mfw_content_words_heatmap_ranked_greyscale.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Heatmap successfully saved as '{output_file}'")
    plt.close()

if __name__ == "__main__":
    main()