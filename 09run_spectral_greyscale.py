#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Performs spectral embedding on a corpus of 5 Russian text files
to visualize stylistic similarity in 2D.

This version is styled for greyscale journal publication and uses
specific labels for the plot.
"""

import os
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import spectral_embedding

# --- 1. Load the Data ---
def load_corpus(filenames: list) -> (list, list):
    """
    Loads text content from a list of files.
    
    Returns:
        (corpus_texts, labels)
    """
    corpus_texts = []
    labels = []
    
    print("--- Step 1: Loading Data ---")
    try:
        for filepath in filenames:
            with open(filepath, 'r', encoding='utf-8') as f:
                corpus_texts.append(f.read())
                
                # Create a clean label from the filename for plotting
                label = os.path.basename(filepath).split('_clean_lemmatized.txt')[0]
                labels.append(label)
                print(f"Loaded: {filepath}")
                
        return corpus_texts, labels
        
    except FileNotFoundError as e:
        print(f"ERROR: File not found.")
        print(f"Details: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred during file loading: {e}")
        return None, None

def main():
    # --- FIXED: Using the correct filenames from our pipeline ---
    filenames = [
        "Ru1_clean_lemmatized.txt",
        "Ru2_clean_lemmatized.txt",
        "Ru3_clean_lemmatized.txt",
        "Ru4_clean_lemmatized.txt",
        "Ru5_clean_lemmatized.txt"
    ]

    corpus, labels = load_corpus(filenames)
    
    if corpus is None:
        print("Halting execution due to file loading error.")
        return

    # Overwrite the simple labels with the ones we want on the plot.
    print("Overriding labels for publication plot...")
    labels = [
        "Ru-1911-Engelgardt",
        "Ru-1926-Anon",
        "Ru-1933-Chukovsky-(Ed.)",
        "Ru-1949-Braude",
        "Ru-1960-Daruzes"
    ]

    # --- 2. Vectorize the Corpus ---
    print("\n--- Step 2: Vectorizing Corpus (TF-IDF) ---")
    # Using TF-IDF is a different (and valid) approach than our raw-count DTMs
    vectorizer = TfidfVectorizer()
    dtm = vectorizer.fit_transform(corpus)
    print(f"Document-Term Matrix (DTM) created with shape: {dtm.shape}")

    # --- 3. Build the Affinity Matrix ---
    print("\n--- Step 3: Building Affinity Matrix (Cosine Similarity) ---")
    affinity_matrix = cosine_similarity(dtm)
    print(f"Affinity Matrix created with shape: {affinity_matrix.shape}")

    # --- 4. Perform Spectral Embedding ---
    print("\n--- Step 4: Performing Spectral Embedding ---")
    embedding = spectral_embedding(
        affinity_matrix,
        n_components=2,
        random_state=42
    )
    print(f"Embedding created with shape: {embedding.shape}")

    # --- 5. Plot the Results (STYLED FOR GREYSCALE) ---
    print("\n--- Step 5: Plotting Results (Greyscale) ---")
    
    plt.style.use('grayscale')
    plt.figure(figsize=(10, 7))
    
    x_coords = embedding[:, 0]
    y_coords = embedding[:, 1]
    
    plt.scatter(
        x_coords, 
        y_coords, 
        s=150,
        color='black',
        alpha=0.75,
        edgecolor='grey'
    )
    
    # create specific labels
    for i, label in enumerate(labels):
        plt.annotate(
            label,
            (x_coords[i], y_coords[i]),
            textcoords="offset points",
            xytext=(7, 7),
            ha='left',
            fontsize=11
        )

    plt.title("Spectral Embedding of Russian Translations", fontsize=16)
    plt.xlabel("Component 1", fontsize=12)
    plt.ylabel("Component 2", fontsize=12)
    
    output_image_file = "spectral_embedding_plot_greyscale.png"
    plt.savefig(
        output_image_file, 
        dpi=300,
        bbox_inches='tight'
    )
    
    print(f"Greyscale plot successfully saved as '{output_image_file}'")
    plt.show()

if __name__ == "__main__":
    main()