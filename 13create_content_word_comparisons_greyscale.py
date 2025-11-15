import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# --- Use the same label mapping as before ---
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def create_mfw_heatmap(directory: str = '.'):
    """
    Creates a combined greyscale heatmap with words sorted by total frequency.
    """
    print("--- Generating combined MFW heatmap ---")
    all_freqs = {}
    master_word_list = set()

    # Step 1: Gather frequencies and a master list of top words
    for filename in sorted([f for f in os.listdir(directory) if f.endswith('_features.json')]):
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)

        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mfw_data = data.get('mfw_frequencies', [])
        if not mfw_data:
            continue
        
        all_freqs[new_label] = {word: count for word, count in mfw_data}
        master_word_list.update([word for word, count in mfw_data[:15]])

    # Step 2: Build a long-format DataFrame for processing
    plot_data = []
    for word in sorted(list(master_word_list)):
        for translation_label, freqs in all_freqs.items():
            count = freqs.get(word, 0)
            plot_data.append({'Word': word, 'Translation': translation_label, 'Frequency': count})

    df_long = pd.DataFrame(plot_data)

    # Step 3: Calculate total frequency and reorder the data
    # Create a list of words sorted by their total frequency (highest first)
    sorted_words = df_long.groupby('Word')['Frequency'].sum().sort_values(ascending=False).index

    # Pivot the data into a grid format
    df_wide = df_long.pivot(index='Word', columns='Translation', values='Frequency')

    # Reorder the rows of the grid according to our sorted list
    df_wide_sorted = df_wide.loc[sorted_words]

    # Step 4: Create the heatmap using the newly sorted data
    plt.figure(figsize=(12, 16))
    sns.heatmap(
        df_wide_sorted,
        annot=True,
        fmt='g',
        cmap='Greys',
        linewidths=.5,
        linecolor='black'
    )
    
    plt.title('Frequency of Top Content Words Across Translations', fontsize=18)
    plt.xlabel('Translation', fontsize=14)
    plt.ylabel('Word (Sorted by Total Frequency)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('mfw_combined_heatmap_greyscale_sorted.png')
    print("Sorted greyscale heatmap saved to mfw_combined_heatmap_greyscale_sorted.png")


if __name__ == '__main__':
    create_mfw_heatmap()