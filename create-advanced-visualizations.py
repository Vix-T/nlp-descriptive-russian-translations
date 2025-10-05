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

def plot_mfw_with_stopwords(directory: str = '.'):
    """
    Plots the top 25 most frequent words, INCLUDING stop words.
    """
    print("--- Generating MFW plots (with stop words) ---")
    sns.set_style("whitegrid")

    for filename in sorted([f for f in os.listdir(directory) if f.endswith('_features.json')]):
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)

        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Load the full unigram frequencies
        unigram_data = data.get('unigram_frequencies', {})
        if not unigram_data:
            continue

        # Convert to a Counter to easily get the most common words
        mfw = Counter(unigram_data).most_common(25)
        
        words = [item[0] for item in mfw]
        counts = [item[1] for item in mfw]

        plt.figure(figsize=(12, 10))
        sns.barplot(x=counts, y=words, palette="cividis", orient='h')
        plt.title(f'Top 25 Words (Including Stop Words) in {new_label}', fontsize=16)
        plt.xlabel('Frequency Count', fontsize=12)
        plt.ylabel('Word', fontsize=12)
        plt.tight_layout()
        
        output_filename = f'mfw_with_stopwords_{book_name}.png'
        plt.savefig(output_filename)
        print(f"✅ Saved plot to {output_filename}")


def plot_mfw_without_stopwords(directory: str = '.'):
    """
    Plots the top 25 most frequent content words (stop words removed).
    """
    print("\n--- Generating MFW plots (without stop words) ---")
    sns.set_style("whitegrid")

    for filename in sorted([f for f in os.listdir(directory) if f.endswith('_features.json')]):
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)

        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mfw_data = data.get('mfw_frequencies', [])
        if not mfw_data:
            continue
        
        # Get the top 25 words for plotting
        top_n = 25
        words = [item[0] for item in mfw_data[:top_n]]
        counts = [item[1] for item in mfw_data[:top_n]]

        plt.figure(figsize=(12, 10))
        sns.barplot(x=counts, y=words, palette="plasma", orient='h')
        plt.title(f'Top {top_n} Most Frequent Content Words in {new_label}', fontsize=16)
        plt.xlabel('Frequency Count', fontsize=12)
        plt.ylabel('Word', fontsize=12)
        plt.tight_layout()
        
        output_filename = f'mfw_no_stopwords_{book_name}.png'
        plt.savefig(output_filename)
        print(f"✅ Saved plot to {output_filename}")


def plot_combined_mfw_comparison(directory: str = '.'):
    """
    Creates a single, combined bar chart comparing the frequency of key
    content words across all five translations.
    """
    print("\n--- Generating combined MFW comparison plot ---")
    all_freqs = {}
    master_word_list = set()

    # Step 1: Gather frequencies and a master list of top words from all texts
    for filename in sorted([f for f in os.listdir(directory) if f.endswith('_features.json')]):
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)

        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mfw_data = data.get('mfw_frequencies', [])
        if not mfw_data:
            continue
        
        # Store all frequencies for this book
        all_freqs[new_label] = {word: count for word, count in mfw_data}
        
        # Add the top 15 words to our master comparison list
        master_word_list.update([word for word, count in mfw_data[:15]])

    # Step 2: Build a DataFrame for plotting
    plot_data = []
    for word in sorted(list(master_word_list)):
        for translation_label, freqs in all_freqs.items():
            # Get the frequency of the word, defaulting to 0 if not found
            count = freqs.get(word, 0)
            plot_data.append({'Word': word, 'Translation': translation_label, 'Frequency': count})

    df = pd.DataFrame(plot_data)

    # Step 3: Create the plot
    plt.figure(figsize=(15, 20))
    sns.barplot(x='Frequency', y='Word', hue='Translation', data=df, orient='h')
    plt.title('Comparison of Frequent Content Words Across Translations', fontsize=18)
    plt.xlabel('Frequency Count', fontsize=14)
    plt.ylabel('Word', fontsize=14)
    plt.legend(title='Translation')
    plt.tight_layout()
    plt.savefig('mfw_combined_comparison.png')
    print("✅ Saved combined comparison plot to mfw_combined_comparison.png")


if __name__ == '__main__':
    plot_mfw_with_stopwords()
    plot_mfw_without_stopwords()
    plot_combined_mfw_comparison()