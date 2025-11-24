#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parses mfinder output files, calculates the L2-Normalized Significance Profile (SP),
and generates a greyscale grouped bar chart for KEY motifs.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib
import re
import numpy as np
from sklearn.preprocessing import Normalizer
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def parse_zscores_from_file(filepath: pathlib.Path) -> dict:
    """
    Parses an mfinder '_OUT.txt' file to extract ALL motif IDs and Z-Scores.
    """
    data = {}
    data_block_found = False
    
    try:
        file_content = filepath.read_text(encoding='utf-8')
        lines = file_content.splitlines()

        for line in lines:
            line = line.strip()
            if not line: continue

            if "Full list of subgraphs size 3 ids:" in line:
                data_block_found = True
                continue
            
            if data_block_found and line[0].isdigit():
                try:
                    parts = line.split()
                    if len(parts) >= 4:
                        motif_id = int(parts[0])
                        z_score = float(parts[3])
                        data[motif_id] = z_score
                except (ValueError, IndexError):
                    continue
    except Exception as e:
        print(f"ERROR: Failed to parse {filepath}: {e}")
    
    return data

def main():
    # --- 1. Setup ---
    data_folder = pathlib.Path('mfinder-analysis')
    
    filenames = [f'Ru{i}_mfinder_input_OUT.txt' for i in range(1, 6)]
    
    # Key motifs to plot
    key_motifs_to_plot = [6, 12, 36] 
    
    translation_map = {
        'Ru1': 'Ru-1911-Engelgardt',
        'Ru2': 'Ru-1926-Anon',
        'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
        'Ru4': 'Ru-1949-Braude',
        'Ru5': 'Ru-1960-Daruzes'
    }

    # --- 2. Parse ALL Data First ---
    print("--- Parsing all Z-Scores... ---")
    
    all_data_rows = []
    index_labels = []

    for filename in filenames:
        short_name = filename.split('_')[0] # Gets "Ru1" from "Ru1_mfinder..."
        full_name = translation_map.get(short_name, short_name)
        file_path = data_folder / filename
        
        motif_data = parse_zscores_from_file(file_path)
        
        if motif_data:
            all_data_rows.append(motif_data)
            index_labels.append(full_name)
        else:
            print(f"Warning: No data found for {filename}")

    if not all_data_rows:
        print("ERROR: No data extracted. Halting.")
        return

    # Create DataFrame of RAW Z-scores
    df_raw = pd.DataFrame(all_data_rows, index=index_labels).fillna(0)

    # --- 3. Apply L2 Normalization ---
    print("--- Normalizing to Significance Profile (SP)... ---")
    transformer = Normalizer(norm='l2')
    sp_data = transformer.fit_transform(df_raw)
    df_sp = pd.DataFrame(sp_data, index=df_raw.index, columns=df_raw.columns)

    # --- 4. Filter & Reshape ---
    df_plot = df_sp[key_motifs_to_plot].reset_index()
    df_plot = df_plot.melt(id_vars='index', var_name='Motif ID', value_name='Normalized Z-Score')
    df_plot = df_plot.rename(columns={'index': 'Translation'})
    df_plot['Motif ID'] = df_plot['Motif ID'].apply(lambda x: f"Motif {x}")

  # --- 5. Plotting ---
    print("--- Generating plot... ---")
    plt.style.use('grayscale')
    sns.set_context("paper", font_scale=1.2)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8)) 
    
    # Define sorting order
    motif_labels = [f"Motif {m}" for m in key_motifs_to_plot]
    
    # Draw Barplot
    sns.barplot(
        data=df_plot,
        x='Motif ID',
        y='Normalized Z-Score',
        hue='Translation',
        palette='Greys_r',
        edgecolor='black',
        order=motif_labels,
        ax=ax
    )
    
    # Add bar values
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3, fontsize=9)

    # --- NEW: Side Panel Icons (The Visual Legend) ---
    
    def add_side_icon(ax, motif_id, y_pos):
        """
        Places a large icon and label on the right-hand side of the plot.
        """
        try:
            file_id = str(motif_id).zfill(2)
            icon_path = f"motif_{file_id}_icon.png"
            img = plt.imread(icon_path)
            
            # 1. Create Image
            imagebox = OffsetImage(img, zoom=0.35) 
            
            # 2. Place Icon
            ab = AnnotationBbox(imagebox, (1.18, y_pos),
                                xycoords='axes fraction',
                                frameon=False,
                                box_alignment=(0.5, 0.5))
            ax.add_artist(ab)
            
            # 3. Add Label Text Below Icon
            # CHANGED: Added zorder=20 to force text on TOP of any overlapping images
            ax.text(1.18, y_pos - 0.13, f"Motif {motif_id}", 
                    transform=ax.transAxes, 
                    ha='center', va='top', fontsize=11, fontweight='bold', color='#333333',
                    zorder=20) 

        except FileNotFoundError:
            print(f"Warning: Icon not found for Motif {motif_id}")

    # Vertical positions for the icons
    # Tweaked slightly to spacing: [0.68, 0.41, 0.14]
    icon_positions = [0.68, 0.41, 0.14]
    
    for m_id, y_pos in zip(key_motifs_to_plot, icon_positions):
        add_side_icon(ax, m_id, y_pos)

    # -------------------------------------------------------

    # Plot Formatting
    plt.title('Key Structural Preferences by Translator', fontsize=18, pad=20)
    plt.ylabel('L2 Normalized Z-Score (Vector Length = 1)', fontsize=13)
    plt.xlabel('Key Network Motif ID', fontsize=13)
    
    # Main Legend 
    plt.legend(title='Translation', bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10, title_fontsize=12)
    plt.axhline(0, color='black', linewidth=0.8)

    # Adjust layout
    plt.subplots_adjust(right=0.80)

    output_file = 'key_motifs_grouped_bar_greyscale_normalized.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Plot successfully saved as '{output_file}'")
    plt.close()

if __name__ == "__main__":
    main()