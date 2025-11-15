import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from collections import Counter

# --- Use the same label mapping as before ---
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def create_all_words_heatmap(directory: str = '.'):
    """
    Creates a combined greyscale heatmap for all words (including stopwords),
    sorted by total frequency.
    """
    print("--- Generating 'All Words' MFW heatmap ---")
    all_freqs = {}
    
    # --- Step 1: Gather ALL unigram frequencies from the JSON files ---
    for filename in sorted([f for f in os.listdir(directory) if f.endswith('_features.json')]):
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)

        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # We now use 'unigram_frequencies' which includes all words
        unigram_data = data.get('unigram_frequencies', {})
        if not unigram_data:
            continue
        
        all_freqs[new_label] = unigram_data

    # --- Step 2: Identify the most frequent words across ALL texts combined ---
    # Combine all frequencies into one large counter
    total_counts = Counter()
    for text_freqs in all_freqs.values():
        total_counts.update(text_freqs)
    
    # Select the top N words to display on the heatmap (to keep it readable)
    top_n_words = 30
    master_word_list = [word for word, count in total_counts.most_common(top_n_words)]

    # --- Step 3: Build a long-format DataFrame for plotting ---
    plot_data = []
    for word in master_word_list:
        for translation_label, freqs in all_freqs.items():
            count = freqs.get(word, 0)
            plot_data.append({'Word': word, 'Translation': translation_label, 'Frequency': count})

    df_long = pd.DataFrame(plot_data)

    # --- Step 4: Pivot and sort the data for the heatmap ---
    df_wide = df_long.pivot(index='Word', columns='Translation', values='Frequency')
    # Reorder the rows to match the master frequency list (most frequent at top)
    df_wide_sorted = df_wide.loc[master_word_list]

    # Step 5: Create the heatmap
    plt.figure(figsize=(12, 16))
    sns.heatmap(
        df_wide_sorted,
        annot=True,
        fmt='g',
        cmap='Greys',
        linewidths=.5,
        linecolor='black'
    )
    
    plt.title(f'Frequency of Top {top_n_words} Words (Including Stopwords)', fontsize=18)
    plt.xlabel('Translation', fontsize=14)
    plt.ylabel('Word (Sorted by Total Frequency)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('mfw_all_words_heatmap_greyscale.png')
    print("'All Words' greyscale heatmap saved to mfw_all_words_heatmap_greyscale.png")


if __name__ == '__main__':
    create_all_words_heatmap()