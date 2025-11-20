#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calculates Betweenness Centrality using the existing mfinder input files.
This ensures 100% consistency with the network used for motif analysis.

Outputs:
1. CSV of all words ranked by Betweenness.
2. Greyscale Bar Chart of the Top 20 Bridge Words.
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import pathlib

def load_network_and_map(input_file: pathlib.Path, map_file: pathlib.Path):
    """
    Loads the mfinder input file as a NetworkX Directed Graph
    and loads the Word-to-ID mapping.
    """
    # 1. Load the JSON Dictionary (Word -> ID)
    try:
        with open(map_file, 'r', encoding='utf-8') as f:
            word_to_id = json.load(f)
        # Flip it to ID -> Word (e.g., {1: "the", 2: "and"})
        id_to_word = {int(v): k for k, v in word_to_id.items()}
    except Exception as e:
        print(f"ERROR loading map {map_file}: {e}")
        return None, None

    # 2. Build the Graph from the numeric edge list
    G = nx.DiGraph()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Format: SourceID TargetID Weight
                parts = line.strip().split()
                if len(parts) == 3:
                    u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                    
                    # NetworkX Betweenness calculation uses 'weight' as DISTANCE.
                    # High frequency (w) = Short distance.
                    # We invert the weight so that strong connections are "close".
                    dist = 1.0 / w if w > 0 else 1.0
                    
                    G.add_edge(u, v, weight=dist)
    except Exception as e:
        print(f"ERROR loading network {input_file}: {e}")
        return None, None

    return G, id_to_word

def main():
    # --- Setup ---
    # We look in the conceptual-analysis folder
    data_folder = pathlib.Path('conceptual-analysis')
    
    translation_map = {
        'Ru1': 'Ru-1911-Engelgardt',
        'Ru2': 'Ru-1926-Anon',
        'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
        'Ru4': 'Ru-1949-Braude',
        'Ru5': 'Ru-1960-Daruzes'
    }
    
    print("--- Starting Betweenness Analysis (Using Existing Networks) ---")

    # Loop through all 5 books
    for i in range(1, 6):
        book_key = f"Ru{i}"
        print(f"\nProcessing {book_key}...")
        
        # Look for the files created by Script 18
        input_file = data_folder / f"{book_key}_mfinder_input.txt"
        map_file = data_folder / f"{book_key}_word_id_mapping.json"
        
        if not input_file.exists() or not map_file.exists():
            print(f"   Skipping {book_key} (Files not found)")
            continue
            
        # 1. Load Graph
        G, id_to_word = load_network_and_map(input_file, map_file)
        if G is None: continue
        
        print(f"   Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
        
        # 2. Calculate Betweenness Centrality
        print("   Calculating betweenness (this takes time for dense networks)...")
        # We use the 'weight' parameter which we set to (1/frequency)
        betweenness = nx.betweenness_centrality(G, weight='weight')
        
        # 3. Convert IDs back to Words
        results = []
        for node_id, score in betweenness.items():
            # Translate ID -> Word
            word = id_to_word.get(node_id, f"ID_{node_id}")
            results.append({'Word': word, 'Betweenness': score})
            
        # 4. Sort and Save
        df = pd.DataFrame(results).sort_values(by='Betweenness', ascending=False)
        
        csv_output = data_folder / f"{book_key}_betweenness_rankings.csv"
        df.to_csv(csv_output, index=False)
        print(f"   Saved rankings to {csv_output}")
        
        # 5. Visualize Top 20
        top_20 = df.head(20)
        
        plt.figure(figsize=(10, 8))
        sns.set_style("whitegrid")
        
        ax = sns.barplot(
            data=top_20,
            x='Betweenness',
            y='Word',
            color='grey',
            edgecolor='black'
        )
        
        # Add value labels to the bars
        # We use a smaller font and 4 decimal places because centrality scores are small
        for container in ax.containers:
            ax.bar_label(container, fmt='%.4f', padding=3, fontsize=8)
        
        full_name = translation_map.get(book_key, book_key)
        plt.title(f'Top 20 "Bridge Words" by Betweenness Centrality\n({full_name})', fontsize=14)
        plt.xlabel('Betweenness Score (Higher = More Central)', fontsize=12)
        plt.ylabel('Word', fontsize=12)
        plt.tight_layout()
        
        plot_output = data_folder / f"{book_key}_betweenness_top20_greyscale.png"
        plt.savefig(plot_output, dpi=300)
        plt.close()
        print(f"   Saved plot to {plot_output}")

    print("\n--- Analysis Complete ---")

if __name__ == "__main__":
    main()