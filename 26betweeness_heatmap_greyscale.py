#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a greyscale heatmap of the *ranks* of the top Betweenness Centrality words.
This allows for a fair comparison between full and abridged texts by comparing
hierarchy rather than raw centrality scores.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pathlib

def main():
    # --- 1. Setup ---
    # Look in the conceptual-analysis folder where we saved the CSVs
    data_folder = pathlib.Path('conceptual-analysis')
    
    translation_map = {
        'Ru1': 'Ru-1911-Engelgardt',
        'Ru2': 'Ru-1926-Anon',
        'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
        'Ru4': 'Ru-1949-Braude',
        'Ru5': 'Ru-1960-Daruzes'
    }
    
    print("--- Building Betweenness Rank DataFrame... ---")

    # We will collect the Top 20 words from EVERY book to make a master list
    master_word_set = set()
    book_data = {}

    for i in range(1, 6):
        book_key = f"Ru{i}"
        csv_path = data_folder / f"{book_key}_betweenness_rankings.csv"
        
        if not csv_path.exists():
            print(f"Warning: {csv_path} not found.")
            continue
            
        # Load the pre-calculated rankings
        df = pd.read_csv(csv_path)
        
        # Create a 'Rank' column (1, 2, 3...)
        # The CSV is already sorted by score descending, so the index+1 is the rank
        df['Rank'] = df.index + 1
        
        # Get the Top 20 words for this specific book
        top_20 = df.head(20)
        master_word_set.update(top_20['Word'].tolist())
        
        # Store the full rank data for lookup later
        # We create a dictionary: {'word': rank, 'word2': rank...}
        book_data[translation_map[book_key]] = dict(zip(df['Word'], df['Rank']))

    # --- 2. Create the Matrix ---
    # Columns = The union of all Top 20 words
    # Rows = Translators
    
    # Sort words alphabetically or by total popularity? 
    # Let's sort by "Average Rank" so the most consistently important words are on the left.
    
    # Helper to get avg rank
    def get_avg_rank(word):
        ranks = [data.get(word, 1000) for data in book_data.values()] # 1000 penalty if missing
        return sum(ranks) / len(ranks)

    sorted_columns = sorted(list(master_word_set), key=get_avg_rank)
    
    # If the list is too long (e.g. >30), slice it to keep the plot readable
    if len(sorted_columns) > 30:
        sorted_columns = sorted_columns[:30]
    
    df_plot = pd.DataFrame(index=book_data.keys(), columns=sorted_columns)
    
    # Fill the matrix
    for translator, ranks in book_data.items():
        for word in sorted_columns:
            # Get rank, if word isn't in the list (rare), give it a high rank (e.g. >100)
            # to show it's not important for this translator.
            df_plot.loc[translator, word] = ranks.get(word, 100)

    # Ensure data is numeric
    df_plot = df_plot.astype(int)

    # --- 3. Plotting ---
    print("--- Generating heatmap... ---")
    
    plt.figure(figsize=(20, 8))
    
    # Create the heatmap
    # We use 'Greys_r' (Reversed) so Rank 1 (Low number) is DARK/BLACK
    # and Rank 100 (High number) is WHITE/LIGHT
    sns.heatmap(
        df_plot,
        cmap="Greys_r", 
        annot=True,
        fmt="d",
        linewidths=.5,
        cbar_kws={'label': 'Betweenness Rank (1 = Most Central)'}
    )

    plt.title('Comparative Rank of Top Bridge Words\nBetweeness Centrality Ranking', fontsize=16, pad=20)
    plt.ylabel('Translation', fontsize=12)
    plt.xlabel('Bridge Words (Sorted by Consistency)', fontsize=12)
    plt.yticks(rotation=0)
    plt.xticks(rotation=45, ha='right')

    output_file = data_folder / 'betweenness_rank_heatmap_greyscale.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Heatmap saved to {output_file}")
    plt.close()

if __name__ == "__main__":
    main()