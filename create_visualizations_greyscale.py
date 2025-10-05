import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Correct labels retrieved from our previous conversation ---
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}


def plot_summary_metrics_greyscale(df: pd.DataFrame):
    """
    Creates GREYSCALE bar charts for TTR and Avg. Sentence Length with custom labels.
    """
    # Use the mapping to rename the index of the DataFrame for plotting
    df = df.rename(index=label_mapping)
    
    sns.set_style("whitegrid")

    # --- Plot 1: TTR in Greyscale with Custom Labels ---
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=df.index, 
        y=df['chunked_ttr'], 
        color='darkgrey',
        edgecolor='black'
    )
    plt.title('Lexical Diversity (Chunked Type-Token Ratio)', fontsize=16)
    plt.xlabel('Translation', fontsize=12)
    plt.ylabel('TTR Score (Higher is More Diverse)', fontsize=12)
    plt.xticks(rotation=45, ha='right') # Rotate labels to prevent overlap
    plt.tight_layout()
    plt.savefig('ttr_comparison_greyscale_labeled.png')
    print("✅ Saved labeled greyscale TTR plot to ttr_comparison_greyscale_labeled.png")

    # --- Plot 2: Sentence Length in Greyscale with Custom Labels ---
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=df.index, 
        y=df['avg_sentence_length'], 
        color='lightgrey',
        edgecolor='black'
    )
    plt.title('Syntactic Complexity (Average Sentence Length)', fontsize=16)
    plt.xlabel('Translation', fontsize=12)
    plt.ylabel('Average Words per Sentence', fontsize=12)
    plt.xticks(rotation=45, ha='right') # Rotate labels to prevent overlap
    plt.tight_layout()
    plt.savefig('sentence_length_comparison_greyscale_labeled.png')
    print("✅ Saved labeled greyscale sentence length plot to sentence_length_comparison_greyscale_labeled.png")


if __name__ == '__main__':
    summary_csv_path = 'stylometric_summary.csv'
    if os.path.exists(summary_csv_path):
        summary_df = pd.read_csv(summary_csv_path).set_index('translation')
        plot_summary_metrics_greyscale(summary_df)
    else:
        print(f"❌ Error: '{summary_csv_path}' not found.")