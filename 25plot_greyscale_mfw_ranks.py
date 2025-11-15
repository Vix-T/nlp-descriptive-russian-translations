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
            # Read the text and split it by spaces
            return f.read().split()
    except FileNotFoundError:
        print(f"❌ ERROR: File not found at {filepath}")
        return []
    except Exception as e:
        print(f"❌ ERROR: Failed to parse {filepath}. Reason: {e}")
        return []

def main():
    # --- 1. Define Data and File Locations ---
    
    data_folder = pathlib.Path('.') # Use '.' for current folder
    
    # --- THIS IS THE FIX ---
    # Updated the filenames to match your new convention
    filenames = {
        'Ru-1911-Engelgardt': 'Ru1_clean_lemmatized_nostops.txt',
        'Ru-1926-Anon': 'Ru2_clean_lemmatized_nostops.txt',
        'Ru-1933-Chukovsky-(Ed.)': 'Ru3_clean_lemmatized_nostops.txt',
        'Ru-1949-Braude': 'Ru4_clean_lemmatized_nostops.txt',
        'Ru-1960-Daruzes': 'Ru5_clean_lemmatized_nostops.txt'
    }
    # --- END OF FIX ---
    
    # --- 2. Calculate Frequencies ---
    print("--- Calculating word frequencies... ---")
    
    all_tokens = []
    book_freqs = {}
    
    for translator, filename in filenames.items():
        file_path = data_folder / filename
        tokens = load_tokens_from_file(file_path)
        
        if not tokens:
            continue
            
        # Store this book's frequency Counter
        book_freqs[translator] = Counter(tokens)
        
        # Add all tokens to one giant list to find the overall top words
        all_tokens.extend(tokens)

    if not all_tokens:
        print("❌ CRITICAL ERROR: No tokens were loaded from any file. Halting.")
        return

    # --- 3. Find Top 30 Overall Content Words ---
    
    # Get the 30 most common words across all texts combined
    overall_freq = Counter(all_tokens)
    top_30_words = [word for word, count in overall_freq.most_common(30)]

    # --- 4. Build the Rank DataFrame ---
    print("--- Building Rank DataFrame... ---")
    
    # Create an empty DataFrame to hold the raw frequencies
    df_freq = pd.DataFrame(columns=top_30_words, index=list(filenames.keys()))
    
    # Populate the DataFrame with the raw counts
    for translator, freqs in book_freqs.items():
        for word in top_30_words:
            # Get the count from this translator's freqs, default to 0
            df_freq.loc[translator, word] = freqs.get(word, 0)

    # --- THIS IS THE KEY STEP ---
    # Convert raw frequencies to ranks.
    # axis=1 ranks horizontally (across the words for each book)
    # ascending=False makes the most frequent word Rank 1
    # Use method='min' to handle ties (e.g., 1, 2, 2, 4)
    df_ranks = df_freq.rank(axis=1, ascending=False, method="min")
    
    # --- 5. Draw the Heatmap ---
    print("--- Generating heatmap... ---")

    plt.figure(figsize=(20, 8))
    
    sns.heatmap(
        df_ranks,
        cmap="Greys",       # Use greyscale colormap
        annot=True,         # Show the rank number
        fmt=".0f",          # Format numbers as integers
        linewidths=.5,
        cbar_kws={'label': 'Frequency Rank (1 = Most Frequent)'} # Updated label
    )

    # --- 6. Customize Plot Labels ---
    
    # Updated title
    plt.title('Relative Rank of Most Frequent Content Words', fontsize=16, pad=20)
    plt.ylabel('Translation', fontsize=12)
    plt.xlabel('Top 30 Content Words (Overall)', fontsize=12)
    plt.yticks(rotation=0)
    plt.xticks(rotation=45, ha='right') # Rotate word labels

    # --- 7. Save and Show ---
    
    output_file = 'mfw_content_words_heatmap_ranked_greyscale.png'
    try:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Heatmap successfully saved as '{output_file}'")
    except Exception as e:
        print(f"❌ ERROR saving file: {e}")
    
    plt.close()

if __name__ == "__main__":
    main()