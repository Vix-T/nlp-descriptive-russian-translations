import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from collections import Counter

# --- Use the final, correct label mapping ---
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def plot_mfw_greyscale_barchart(words: list, counts: list, plot_title: str, output_filename: str):
    """A reusable function to create one greyscale horizontal bar chart."""
    plt.figure(figsize=(12, 10))
    sns.barplot(
        x=counts, 
        y=words, 
        color='darkgrey',
        edgecolor='black',
        orient='h'
    )
    plt.title(plot_title, fontsize=16)
    plt.xlabel('Frequency Count', fontsize=12)
    plt.ylabel('Word', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_filename)
    # Close the plot to free up memory before the next one is created
    plt.close()
    print(f"Saved plot to {output_filename}")


if __name__ == '__main__':
    print("--- Generating Top 20 MFW Greyscale Plots ---")
    
    # You can easily change this number to get a different "Top N"
    top_n = 20
    
    # Find all feature files in the current directory
    json_files = sorted([f for f in os.listdir('.') if f.endswith('_features.json')])

    # Loop through each feature file
    for filename in json_files:
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # --- Plot 1: WITH Stopwords ---
        unigram_data = data.get('unigram_frequencies', {})
        if unigram_data:
            mfw_with_stops = Counter(unigram_data).most_common(top_n)
            words = [item[0] for item in mfw_with_stops]
            counts = [item[1] for item in mfw_with_stops]
            plot_title = f'Top {top_n} Words (With Stopwords) in {new_label}'
            output_filename = f'mfw_with_stopwords_{book_name}_greyscale.png'
            plot_mfw_greyscale_barchart(words, counts, plot_title, output_filename)

        # --- Plot 2: WITHOUT Stopwords (Content Words) ---
        mfw_data = data.get('mfw_frequencies', [])
        if mfw_data:
            # The mfw_frequencies are already sorted, so we just take the top N
            top_content_words = mfw_data[:top_n]
            words = [item[0] for item in top_content_words]
            counts = [item[1] for item in top_content_words]
            plot_title = f'Top {top_n} Most Frequent Content Words in {new_label}'
            output_filename = f'mfw_no_stopwords_{book_name}_greyscale.png'
            plot_mfw_greyscale_barchart(words, counts, plot_title, output_filename)

    print("\n--- All 10 plots have been generated. ---")