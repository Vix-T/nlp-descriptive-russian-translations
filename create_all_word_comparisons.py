import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from collections import Counter

# Use the same label mapping as before for consistent naming
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def plot_combined_all_words_comparison(directory: str = '.'):
    """
    Creates a single, combined bar chart comparing the frequency of the most
    common words (including stop words) across all five translations.
    """
    print("--- Generating combined 'All Words' comparison plot ---")
    all_freqs = {}
    master_word_counter = Counter()

    # Step 1: Gather all unigram frequencies from all texts
    for filename in sorted([f for f in os.listdir(directory) if f.endswith('_features.json')]):
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)

        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Use 'unigram_frequencies' which contains ALL words
        unigram_data = data.get('unigram_frequencies', {})
        if not unigram_data:
            continue
        
        # Store all frequencies for this book and add to the master counter
        all_freqs[new_label] = unigram_data
        master_word_counter.update(unigram_data)

    # Step 2: Identify the top 20 most frequent words across the entire corpus
    top_words = [word for word, count in master_word_counter.most_common(20)]
    print(f"Identified top {len(top_words)} words across all texts for comparison.")

    # Step 3: Build a DataFrame for plotting only these top words
    plot_data = []
    for word in top_words:
        for translation_label, freqs in all_freqs.items():
            # Get the frequency of the word, defaulting to 0 if not found
            count = freqs.get(word, 0)
            plot_data.append({'Word': word, 'Translation': translation_label, 'Frequency': count})

    df = pd.DataFrame(plot_data)

    # Step 4: Create the plot
    plt.figure(figsize=(15, 12))
    sns.barplot(x='Frequency', y='Word', hue='Translation', data=df, orient='h')
    
    plt.title('Comparison of Top 20 Most Frequent Words (All Words) Across Translations', fontsize=18)
    plt.xlabel('Frequency Count', fontsize=14)
    plt.ylabel('Word', fontsize=14)
    plt.legend(title='Translation')
    plt.tight_layout()
    
    plt.savefig('all_words_combined_comparison.png')
    print("✅ Saved combined comparison plot to all_words_combined_comparison.png")


if __name__ == '__main__':
    plot_combined_all_words_comparison()