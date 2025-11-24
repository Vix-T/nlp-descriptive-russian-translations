#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates a greyscale heatmap of REAL motif Z-scores from the mfinder Network.
Displays Raw Z-Scores to highlight statistical significance.

Features:
- Adds an asterisk (*) to cells where |Z-Score| > 2.0
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import re

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

                # 1. Look for the line that signals the start of the data block
                if "Full list of subgraphs size 3 ids:" in line:
                    data_block_found = True
                    continue
                
                # 2. Once we've found that signal, start looking for data
                if data_block_found:
                    # Skip header lines
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
    # --- 1. Load the REAL Data (mfinder) ---
    
    # FIXED: Pointing to the correct directory
    subdirectory = "mfinder-analysis"
    
    # FIXED: Pointing to the correct filenames
    base_filenames = [f"Ru{i}_mfinder_input_OUT.txt" for i in range(1, 6)]
    files_to_process = [os.path.join(subdirectory, f) for f in base_filenames]
    
    index_labels = [
        'Ru-1911-Engelgardt',
        'Ru-1926-Anon',
        'Ru-1933-Chukovsky-(Ed.)',
        'Ru-1949-Braude',
        'Ru-1960-Daruzes'
    ]
    
    print("--- Parsing Z-Score data (mfinder) ... ---")
    
    data_rows = []
    for label, filepath in zip(index_labels, files_to_process):
        motif_data = parse_zscores_from_file(filepath)
        if not motif_data:
            print(f"Warning: No data extracted from {filepath}.")
            continue
        data_rows.append(motif_data)

    if not data_rows:
        print("ERROR: No data was extracted from any file. Halting.")
        return

    # Create the DataFrame with the numeric data
    df_zscores = pd.DataFrame(data_rows, index=index_labels)
    
    # --- 2. Create Significance Annotations ---
    print("--- Creating significance annotations... ---")
    df_annot = pd.DataFrame(index=df_zscores.index, columns=df_zscores.columns)
    
    # Loop through the numeric data and create the text labels
    for r in df_zscores.index:
        for c in df_zscores.columns:
            z_score = df_zscores.loc[r, c]
            
            # Check if the value is "significant" (Standard Z-score threshold)
            if abs(z_score) > 2.0:
                df_annot.loc[r, c] = f"{z_score:.2f}*" # Add asterisk
            else:
                df_annot.loc[r, c] = f"{z_score:.2f}"
    
    # Rename columns to be "Motif X" for the plot
    df_zscores = df_zscores.rename(columns={
        col: f"Motif {col}" for col in df_zscores.columns
    })
    # Also rename the annotation dataframe's columns
    df_annot.columns = df_zscores.columns
    
    print("--- Data loaded successfully. Generating heatmap... ---")

    # --- 3. Draw the Heatmap ---
    
    plt.figure(figsize=(14, 8))
    
    sns.heatmap(
        df_zscores,        # The numeric data (Raw Z-Scores) for the colors
        cmap="Greys",
        annot=df_annot,    # The text data with asterisks
        fmt="",            # MUST be empty, as we pre-formatted our text
        linewidths=.5,
        cbar_kws={'label': 'Raw Z-Scores: * = |Z-Score| > 2.0 (Significant)'}
    )

    # --- 4. Customize Plot Labels ---
    
    plt.title('Over and Under Representation of Motifs by Translation', fontsize=16, pad=20)
    plt.ylabel('Translation', fontsize=12)
    plt.xlabel('Motif ID', fontsize=12)
    plt.yticks(rotation=0) 

    # --- 5. Save and Show ---
    
    output_file = 'heatmap_greyscale_significant.png'
    try:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Heatmap successfully saved as '{output_file}'")
    except Exception as e:
        print(f"ERROR saving file: {e}")
    
    plt.close()

if __name__ == "__main__":
    main()