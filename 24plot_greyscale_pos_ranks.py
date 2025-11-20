#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a greyscale heatmap of the *ranks* of the most frequent
Part-of-Speech (POS) tags.

This allows us to compare the relative importance of different grammatical
structures across translations, independent of text length.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from collections import Counter

# --- Label Mapping ---
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def main():
    # --- 1. Setup ---
    print("--- Calculating POS Tag Ranks... ---")
    
    # Find all feature files
    directory = '.'
    json_files = sorted([f for f in os.listdir(directory) if f.endswith('_features.json')])
    
    if not json_files:
        print("ERROR: No '_features.json' files found.")
        return

    all_pos_counts = {}
    global_pos_counter = Counter()

    # --- 2. Load Data ---
    for filename in json_files:
        book_key = filename.split('_features.json')[0]
        label = label_mapping.get(book_key, book_key)
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Extract POS frequencies
            # Note: These are the FULL tags (e.g., "VERB,perf,masc...")
            pos_data = data.get('pos_frequencies', {})
            
            if not pos_data:
                print(f"Warning: No POS data in {filename}")
                continue
                
            # Store for this book
            all_pos_counts[label] = pos_data
            
            # Add to global counter to find the Top 10 overall
            global_pos_counter.update(pos_data)
            
        except Exception as e:
            print(f"ERROR reading {filename}: {e}")

    # --- 3. Identify Top 10 POS Tags ---
    # We rank the top 10 most common tags across the entire corpus
    top_10_tags = [tag for tag, count in global_pos_counter.most_common(10)]
    
    if not top_10_tags:
        print("ERROR: No POS tags found.")
        return

    # --- 4. Build Rank DataFrame ---
    print("--- Building Rank DataFrame... ---")
    
    # Create DataFrame (Rows = Translators, Cols = Top 10 Tags)
    df_freq = pd.DataFrame(index=all_pos_counts.keys(), columns=top_10_tags).fillna(0)
    
    # Fill with raw counts
    for label, counts in all_pos_counts.items():
        for tag in top_10_tags:
            df_freq.loc[label, tag] = counts.get(tag, 0)

    # Convert counts to RANKS (1 = Most Frequent)
    # axis=1 ranks across the row (for each translator)
    df_ranks = df_freq.rank(axis=1, ascending=False, method="min")

    # --- 5. Visualization ---
    print("--- Generating Heatmap... ---")
    
    plt.figure(figsize=(14, 8))
    
    sns.heatmap(
        df_ranks,
        cmap="Greys",       
        annot=True,         # Show the rank number
        fmt=".0f",          # Integer format
        linewidths=.5,
        cbar_kws={'label': 'Frequency Rank (1 = Most Frequent)'}
    )

    # --- 6. Formatting ---
    plt.title('Relative Rank of Top 10 Part of Speech Tags', fontsize=16, pad=20)
    plt.ylabel('Translation', fontsize=12)
    plt.xlabel('Top 10 POS Tags Over All Translations', fontsize=12)
    
    # Rotate x-axis labels because full tags can be long
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0)

    # --- 7. Save ---
    output_file = 'pos_rank_heatmap_greyscale.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Heatmap successfully saved as '{output_file}'")
    plt.close()

if __name__ == "__main__":
    main()