#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parses mfinder output files for key motif Z-scores and generates
a greyscale grouped bar chart for journal publication.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib
import re

def main():
    # --- 1. & 2. Define Data and File Locations ---
    
    data_folder = pathlib.Path('syntactic-analysis')
    filenames = [f'Ru{i}_syntactic_output_OUT.txt' for i in range(1, 6)]
    
    # Define the "Key Motifs" we want to plot
    key_motifs = [78, 110, 238]
    
    # Map for the final plot labels
    translation_map = {
        'Ru1': 'Ru-1911-Engelgardt',
        'Ru2': 'Ru-1926-Anon',
        'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
        'Ru4': 'Ru-1949-Braude',
        'Ru5': 'Ru-1960-Daruzes'
    }

    # --- 3. Parse the Data (New Logic) ---
    
    data_for_plot = []
    print("--- Starting to parse Z-Scores for key motifs... ---")
    
    for filename in filenames:
        short_name = filename.split('_')[0]
        full_name = translation_map[short_name]
        file_path = data_folder / filename
        
        try:
            # Read the entire file content
            file_content = file_path.read_text(encoding='utf-8')
            
            # Inner Loop: For each key motif
            for motif_id in key_motifs:
                
                # Use Regex to find the Z-score
                # This looks for: ^[motif_id] [NREAL] [NRAND] [ZSCORE]
                pattern = re.compile(
                    # Line starts with the motif ID
                    r"^" + str(motif_id) + 
                    # Skips NREAL (e.g., 303928)
                    r"\s+\d+\s+" +
                    # Skips NRAND (e.g., 307363.4+-462.6)
                    r"[\d\.\+\-]+\s+" +
                    # Captures the ZSCORE (e.g., -7.43)
                    r"([\-\d\.]+)",
                    re.MULTILINE
                )
                
                match = pattern.search(file_content)
                
                # Store the data
                if match:
                    z_score = float(match.group(1))
                else:
                    print(f"   ⚠️ Warning: Motif {motif_id} not found in {filename}.")
                    z_score = 0.0 # Fallback
                
                # Append the data in "long" format
                data_for_plot.append({
                    'Translation': full_name,
                    'Motif ID': f'Motif {motif_id}',
                    'Z-Score': z_score
                })
        
        except FileNotFoundError:
            print(f"❌ ERROR: File not found at {file_path}")
            continue
        except Exception as e:
            print(f"❌ ERROR: Failed to parse {file_path}. Reason: {e}")
            continue
            
    print(f"✅ Data parsed for {len(filenames)} files.")

    # --- 4. Prepare the DataFrame ---
    
    df = pd.DataFrame(data_for_plot)
    
    if df.empty:
        print("❌ ERROR: No data was extracted. Halting.")
        return
        
    print("--- DataFrame created. Generating plot... ---")

    # --- 5. Plot the Grouped Bar Chart ---
    
    plt.style.use('grayscale')
    sns.set_context("paper", font_scale=1.2)
    
    plt.figure(figsize=(12, 8))
    
    sns.barplot(
        data=df,
        x='Motif ID',    # Groups on the x-axis
        y='Z-Score',
        hue='Translation', # Bars within each group
        palette='Greys_r',
        edgecolor='black'
    )
    
    # --- 6. Customize Labels and Title ---
    
    plt.title('Syntactic Fingerprints of Key Motifs (Z-Scores)', fontsize=16, pad=20)
    plt.ylabel('Z-Score (Significance)', fontsize=12)
    plt.xlabel('Motif ID', fontsize=12)
    
    # Place legend outside the plot
    plt.legend(title='Translation', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Add reference lines
    plt.axhline(0, color='black', linewidth=0.8, linestyle='-')
    plt.axhline(2.0, color='grey', linewidth=0.6, linestyle='--')
    plt.axhline(-2.0, color='grey', linewidth=0.6, linestyle='--')

    # --- 7. Save and Show ---
    
    output_file = 'key_motifs_grouped_bar_greyscale.png'
    try:
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ Plot successfully saved as '{output_file}'")
    except Exception as e:
        print(f"❌ ERROR saving file: {e}")
    
    # Close the figure to free up memory and exit cleanly
    plt.close()

if __name__ == "__main__":
    main()