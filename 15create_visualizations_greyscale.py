import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Correct labels ---
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def plot_summary_metrics_greyscale(df: pd.DataFrame):
    """
    Creates GREYSCALE bar charts for TTR and Avg. Sentence Length.
    """
    # Rename index using the mapping
    df = df.rename(index=label_mapping)
    sns.set_style("whitegrid")

    # --- Plot 1: TTR ---
    plt.figure(figsize=(10, 6))
    ax1 = sns.barplot(x=df.index, y=df['chunked_ttr'], color='darkgrey', edgecolor='black')
    ax1.bar_label(ax1.containers[0], fmt='%.3f', padding=3)
    
    plt.title('Chunked Type-Token Ratio', fontsize=16)
    plt.xlabel('Translation', fontsize=12)
    plt.ylabel('TTR Score (Higher is More Diverse)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('ttr_comparison_greyscale_labeled.png')
    print("Saved TTR plot.")

    # --- Plot 2: Sentence Length ---
    plt.figure(figsize=(10, 6))
    ax2 = sns.barplot(x=df.index, y=df['avg_sentence_length'], color='lightgrey', edgecolor='black')
    ax2.bar_label(ax2.containers[0], fmt='%.1f', padding=3)
    
    plt.title('Average Sentence Length', fontsize=16)
    plt.xlabel('Translation', fontsize=12)
    plt.ylabel('Average Words per Sentence', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('sentence_length_comparison_greyscale_labeled.png')
    print("Saved Sentence Length plot.")

def plot_kw_metrics_greyscale(csv_path: str):
    """
    Creates GREYSCALE bar charts for Yule's K and Honoré's W.
    """
    # Load the CSV
    df = pd.read_csv(csv_path)
    
    # Clean up filenames to match our labels (e.g., "Ru1_clean..." -> "Ru1")
    df['Translation'] = df['Filename'].apply(lambda x: x.split('_')[0])
    df['Translation'] = df['Translation'].map(label_mapping)
    df = df.set_index('Translation')
    
    sns.set_style("whitegrid")

    # --- Plot 3: Yule's K ---
    # Note: Lower Yule's K HIGHER diversity, unlike TTR.
    plt.figure(figsize=(10, 6))
    ax3 = sns.barplot(x=df.index, y=df['Yules_K'], color='silver', edgecolor='black')
    ax3.bar_label(ax3.containers[0], fmt='%.1f', padding=3)
    
    plt.title("Yule's K", fontsize=16)
    plt.xlabel('Translation', fontsize=12)
    plt.ylabel("Yule's K (Lower = Richer Lexical Diversity)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('yules_k_comparison_greyscale_labeled.png')
    print("Saved Yule's K plot.")

    # --- Plot 4: Honoré's W ---
    # Higher W = Richer vocabulary
    plt.figure(figsize=(10, 6))
    ax4 = sns.barplot(x=df.index, y=df['Honores_W'], color='gainsboro', edgecolor='black')
    ax4.bar_label(ax4.containers[0], fmt='%.1f', padding=3)
    
    plt.title("Honoré's W", fontsize=16)
    plt.xlabel('Translation', fontsize=12)
    plt.ylabel("Honoré's W (Higher = Richer Lexical Diversity)", fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('honores_w_comparison_greyscale_labeled.png')
    print("Saved Honoré's W plot.")

if __name__ == '__main__':
    # 1. Plot standard summaries (TTR, Sentence Length)
    summary_csv = 'stylometric_summary.csv'
    if os.path.exists(summary_csv):
        summary_df = pd.read_csv(summary_csv).set_index('translation')
        plot_summary_metrics_greyscale(summary_df)
    else:
        print(f"Error: '{summary_csv}' not found.")

    # 2. Plot advanced richness metrics (Yule's K, Honoré's W)
    kw_csv = 'lexical_diversity_results.csv'
    if os.path.exists(kw_csv):
        plot_kw_metrics_greyscale(kw_csv)
    else:
        print(f"Error: '{kw_csv}' not found (Run script 15 first).")