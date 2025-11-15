import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymorphy2
from collections import Counter
from decimal import Decimal, getcontext
import math

# Set precision for Decimal calculations (for entropy)
getcontext().prec = 50

# --- 1. Text Loading Utility ---

def load_tokens_from_file(filepath: str) -> list:
    """
    Loads a pre-cleaned text file (e.g., 'Ru1_clean_lemmatized.txt')
    and returns its content as a list of tokens.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            # Read the whole file and split it by spaces
            return file.read().split()
    except FileNotFoundError:
        print(f"ERROR: File not found at {filepath}")
        return []
    except Exception as e:
        print(f"ERROR: Failed to read {filepath}. Reason: {e}")
        return []

# --- 2. Text Analysis Functions ---

def get_pos_freqs(tokens: list, morph) -> Counter:
    """Calculates part-of-speech frequencies from lemmatized tokens."""
    pos_tags = []
    for token in tokens:
        p = morph.parse(token)[0]
        # Use the 'short' tag (e.g., NOUN, ADJF, VERB)
        pos = p.tag.POS
        if pos:
            pos_tags.append(pos)
    return Counter(pos_tags)

def calculate_ttr(tokens: list) -> float:
    """Calculates Type-Token Ratio (TTR)."""
    if not tokens:
        return 0.0
    num_tokens = len(tokens)
    num_types = len(set(tokens))
    return num_types / num_tokens

def calculate_entropy(tokens: list) -> Decimal:
    """Calculates Shannon Entropy for a list of tokens."""
    if not tokens:
        return Decimal(0)
    
    token_counts = Counter(tokens)
    total_tokens = Decimal(len(tokens))
    entropy = Decimal(0)
    
    for count in token_counts.values():
        probability = Decimal(count) / total_tokens
        entropy -= probability * probability.ln()
        
    return entropy / Decimal(2).ln() # Convert to bits (log base 2)

# --- 3. Plotting Functions ---

def plot_top_pos(pos_counts: Counter, book_name: str, output_dir: str):
    """Creates and saves a greyscale bar chart of the top 10 POS."""
    top_10 = pos_counts.most_common(10)
    df = pd.DataFrame(top_10, columns=['POS', 'Frequency'])
    
    plt.figure(figsize=(10, 6))
    plt.style.use('grayscale')
    sns.barplot(x='Frequency', y='POS', data=df, color='grey', edgecolor='black')
    
    plt.title(f'Top 10 Part-of-Speech Tags: {book_name}')
    plt.xlabel('Frequency')
    plt.ylabel('Part-of-Speech Tag')
    
    output_path = os.path.join(output_dir, f"{book_name}_pos_distribution.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ... POS chart saved to {output_path}")

def plot_diagnostic_table(stats: list, output_dir: str):
    """Creates and saves a PNG image of the statistics table."""
    df = pd.DataFrame(stats)
    df = df.set_index('Book')
    
    # Format the numbers to 4 decimal places
    df['TTR'] = df['TTR'].map('{:.4f}'.format)
    df['Entropy'] = df['Entropy'].map('{:.4f}'.format)
    
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis('tight')
    ax.axis('off')
    
    the_table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        rowLabels=df.index,
        loc='center',
        cellLoc='center'
    )
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(12)
    the_table.scale(1.2, 1.2)
    
    output_path = os.path.join(output_dir, "diagnostic_stats_table.png")
    plt.title('Lexical Richness Diagnostics (Stopwords Removed)', pad=20)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nDiagnostic table saved to {output_path}")

# --- 4. Main Execution ---

if __name__ == "__main__":
    
    # --- Setup ---
    output_dir = "diagnostics"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    book_names = ['Ru1', 'Ru2', 'Ru3', 'Ru4', 'Ru5']
    
    # Initialize the lemmatizer once
    print("Initializing MorphAnalyzer (this may take a moment)...")
    morph = pymorphy2.MorphAnalyzer()
    print("Analyzer ready.")
    
    diagnostic_stats = []
    all_pos_counts = {}

    print("--- Starting Linguistic Diagnostic ---")

    # --- Analysis Loop ---
    for book_name in book_names:
        print(f"Processing {book_name}...")
        
        # 1. Define the pre-cleaned file paths
        file_with_stops = f"{book_name}_clean_lemmatized.txt"
        file_no_stops = f"{book_name}_clean_lemmatized_nostops.txt"
        
        # 2. Load the tokens
        tokens_with_stops = load_tokens_from_file(file_with_stops)
        tokens_no_stops = load_tokens_from_file(file_no_stops)
        
        if not tokens_with_stops or not tokens_no_stops:
            print(f"   Skipping {book_name} due to missing files.")
            continue
            
        # 3. Analyze POS (using the file with stop words)
        pos_counts = get_pos_freqs(tokens_with_stops, morph)
        all_pos_counts[book_name] = pos_counts
        
        # 4. Calculate lexical stats (using the file without stop words)
        ttr = calculate_ttr(tokens_no_stops)
        entropy = calculate_entropy(tokens_no_stops)
        
        diagnostic_stats.append({
            'Book': book_name,
            'TTR': ttr,
            'Entropy': entropy
        })

    # --- Plotting Loop ---
    print("\n--- Generating Plots ---")
    
    # 1. Create the main table
    if diagnostic_stats:
        plot_diagnostic_table(diagnostic_stats, output_dir)
    else:
        print("   No stats calculated, skipping table plot.")
    
    # 2. Create the individual POS bar charts
    if all_pos_counts:
        for book_name, pos_data in all_pos_counts.items():
            plot_top_pos(pos_data, book_name, output_dir)
    else:
        print("   No POS data found, skipping bar charts.")
        
    print("\n--- Diagnostic complete. ---")