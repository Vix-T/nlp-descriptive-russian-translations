import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# (Your label_mapping and functions are all correct and do not need to be changed)
# ... (Keep all the function code from your script here) ...
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def plot_summary_metrics(df: pd.DataFrame):
    df = df.rename(index=label_mapping)
    sns.set_style("whitegrid")
    palette = sns.color_palette("viridis", len(df))
    plt.figure(figsize=(10, 7))
    sns.barplot(x=df.index, y=df['chunked_ttr'], palette=palette)
    plt.title('Lexical Diversity (Chunked Type-Token Ratio)', fontsize=16)
    plt.xlabel('Translation', fontsize=12)
    plt.ylabel('TTR Score (Higher is More Diverse)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('ttr_comparison_new_labels.png')
    print("✅ Saved TTR comparison plot to ttr_comparison_new_labels.png")
    plt.figure(figsize=(10, 7))
    sns.barplot(x=df.index, y=df['avg_sentence_length'], palette=palette)
    plt.title('Syntactic Complexity (Average Sentence Length)', fontsize=16)
    plt.xlabel('Translation', fontsize=12)
    plt.ylabel('Average Words per Sentence', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('sentence_length_comparison_new_labels.png')
    print("✅ Saved sentence length plot to sentence_length_comparison_new_labels.png")

def plot_most_frequent_words(directory: str = '.'):
    print("\nAttempting to generate Most Frequent Word plots...")
    sns.set_style("whitegrid")
    json_files = [f for f in os.listdir(directory) if f.endswith('_features.json')]
    if not json_files:
        print("   - DIAGNOSTIC: No '_features.json' files were found.")
        return
    print(f"   - DIAGNOSTIC: Found {len(json_files)} feature file(s).")
    for filename in sorted(json_files):
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        mfw_data = data.get('mfw_frequencies', [])
        if not mfw_data:
            continue
        top_n = 15
        words = [item[0] for item in mfw_data[:top_n]]
        counts = [item[1] for item in mfw_data[:top_n]]
        plt.figure(figsize=(12, 8))
        sns.barplot(x=counts, y=words, palette="plasma", orient='h')
        plt.title(f'Top {top_n} Most Frequent Content Words in {new_label}', fontsize=16)
        plt.xlabel('Frequency Count', fontsize=12)
        plt.ylabel('Word', fontsize=12)
        plt.tight_layout()
        output_filename = f'mfw_{book_name}_new_labels.png'
        plt.savefig(output_filename)
        print(f"✅ Saved MFW plot to {output_filename}")


if __name__ == '__main__':
    print("--- DIAGNOSTIC: Script started. ---")
    
    # --- Check for summary CSV file ---
    summary_csv_path = 'stylometric_summary.csv'
    print(f"--- DIAGNOSTIC: Checking for '{summary_csv_path}'... ---")
    
    if os.path.exists(summary_csv_path):
        print(f"   - DIAGNOSTIC: File found! Loading into DataFrame.")
        summary_df = pd.read_csv(summary_csv_path).set_index('translation')
        plot_summary_metrics(summary_df)
    else:
        # This is the most likely reason for the silence.
        print(f"   - DIAGNOSTIC: File NOT found. Skipping summary plots.")

    # --- Check for JSON feature files ---
    plot_most_frequent_words()
    
    print("\n--- DIAGNOSTIC: Script finished. ---")