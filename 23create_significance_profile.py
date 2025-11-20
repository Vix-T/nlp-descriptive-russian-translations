#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a greyscale heatmap of L2-Normalized Significance Profiles (SPs).

HYBRID VISUALIZATION:
- COLORS & NUMBERS: L2 Normalized (Vector Length = 1) to compare 'shape' across translations.
- ASTERISKS (*): Derived from the RAW Z-Scores (|Z| > 2.0) to show true statistical significance.
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from sklearn.preprocessing import Normalizer

def parse_zscores_from_file(filepath: str) -> dict:
    """
    Parses an mfinder '_OUT.txt' file to extract motif IDs and Z-Scores.
    """
    data = {}
    data_block_found = False
    
    if not os.path.exists(filepath):
        print(f"ERROR: File not found at '{filepath}'")
        return data

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if "Full list of subgraphs size 3 ids:" in line:
                    data_block_found = True
                    continue
                
                if data_block_found:
                    if not line[0].isdigit():
                        continue
                    
                    try:
                        parts = line.split()
                        if len(parts) >= 4:
                            motif_id = int(parts[0])
                            z_score = float(parts[3])
                            data[motif_id] = z_score
                    except (ValueError, IndexError):
                        continue
                        
    except Exception as e:
        print(f"ERROR: Failed to parse {filepath}. Reason: {e}")

    return data

def main():
    # --- 1. Load the Z-Score Data (Conceptual) ---
    
    subdirectory = "conceptual-analysis"
    base_filenames = [f"Ru{i}_mfinder_input_OUT.txt" for i in range(1, 6)]
    files_to_process = [os.path.join(subdirectory, f) for f in base_filenames]
    
    index_labels = [
        'Ru-1911-Engelgardt',
        'Ru-1926-Anon',
        'Ru-1933-Chukovsky-(Ed.)',
        'Ru-1949-Braude',
        'Ru-1960-Daruzes'
    ]
    
    print("--- Parsing Raw Z-Scores... ---")
    
    data_rows = []
    for label, filepath in zip(index_labels, files_to_process):
        motif_data = parse_zscores_from_file(filepath)
        if not motif_data:
            print(f"Warning: No data extracted from {filepath}.")
            continue
        data_rows.append(motif_data)

    if not data_rows:
        print("ERROR: No data extracted. Halting.")
        return

    # df_zscores holds the RAW Z-Scores (used for significance check)
    df_zscores = pd.DataFrame(data_rows, index=index_labels).fillna(0)

    # --- 2. Normalize to Create Significance Profile (SP) ---
    print("--- Normalizing Z-Score vectors... ---")
    
    # Apply L2 normalization (Vector Length = 1)
    transformer = Normalizer(norm='l2')
    sp_data = transformer.fit_transform(df_zscores)
    
    # df_sp holds the NORMALIZED values (used for plotting colors/numbers)
    df_sp = pd.DataFrame(sp_data, index=df_zscores.index, columns=df_zscores.columns)

    # Save to CSV for reference
    sp_output_csv = 'significance_profile_conceptual.csv'
    df_sp.to_csv(sp_output_csv)
    print(f"Normalized Significance Profile saved to '{sp_output_csv}'")
    
    # --- 3. Create Hybrid Annotations ---
    # We want to display the NORMALIZED value, but add a '*' if the RAW value was significant.
    
    print("--- Creating hybrid annotations... ---")
    df_annot = pd.DataFrame(index=df_sp.index, columns=df_sp.columns)
    
    for r in df_sp.index:
        for c in df_sp.columns:
            norm_val = df_sp.loc[r, c]    # The number we show
            raw_val = df_zscores.loc[r, c] # The number we check for significance
            
            # Significance Check: Is the RAW score > 2.0 or < -2.0?
            if abs(raw_val) > 2.0:
                df_annot.loc[r, c] = f"{norm_val:.2f}*" # Add asterisk
            else:
                df_annot.loc[r, c] = f"{norm_val:.2f}"

    # --- 4. Plotting ---
    print("--- Generating heatmap... ---")

    # Rename columns for the plot (e.g. "6" -> "Motif 6")
    df_sp = df_sp.rename(columns={col: f"Motif {col}" for col in df_sp.columns})
    df_annot.columns = df_sp.columns # Ensure annot columns match plot columns
    
    plt.figure(figsize=(14, 8))
    
    sns.heatmap(
        df_sp,             # Plot the NORMALIZED data (colors)
        cmap="Greys", 
        annot=df_annot,    # Use our custom HYBRID annotations
        fmt="",            # Must be empty string since df_annot is already strings
        linewidths=.5, 
        cbar_kws={'label': 'Normalized Z-Score (Vector Length = 1)'}
    )

    plt.title('Network Motif Significance Profile L2 Normalized\n* = Raw Z-Score > 2.0 (Statistically Significant)', fontsize=16, pad=20)
    plt.ylabel('Translation', fontsize=12)
    plt.xlabel('Motif ID', fontsize=12)
    plt.yticks(rotation=0) 

    output_file = 'heatmap_significance_profile_greyscale.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"SP Heatmap saved as '{output_file}'")
    plt.close()

if __name__ == "__main__":
    main()