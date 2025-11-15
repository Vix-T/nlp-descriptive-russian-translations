import pandas as pd
from sklearn.metrics.pairwise import cosine_distances
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

def generate_cluster_analysis_greyscale(dtm_filepath: str, output_filename: str, plot_title: str):
    """
    Loads a Document-Term Matrix, performs a Cluster Analysis based on Cosine Distance,
    and saves the resulting greyscale dendrogram.
    """
    print(f"\n--- Running Greyscale Cluster Analysis for: {plot_title} ---")
    
    # Step 1: Load the Document-Term Matrix
    try:
        dtm = pd.read_csv(dtm_filepath, index_col=0)
        print(f"Loaded DTM from '{dtm_filepath}'.")
    except FileNotFoundError:
        print(f"ERROR: File not found at '{dtm_filepath}'.")
        return

    # Step 2: Calculate the stylistic distance between documents.
    # Using the direct cosine_distances function.
    dist_matrix = cosine_distances(dtm)
    
    # Step 3: Perform Hierarchical Clustering.
    # Note: 'ward' linkage requires a distance matrix (which this is).
    linkage_matrix = linkage(dist_matrix, method='ward')

    # Step 4: Create and save the greyscale dendrogram visualization
    plt.figure(figsize=(12, 8))
    dendrogram(
        linkage_matrix,
        labels=dtm.index.tolist(),
        orientation='right',
        leaf_font_size=12,
        # This function forces all branches of the tree to be black
        link_color_func=lambda k: 'black'
    )

    plt.title(plot_title, fontsize=16)
    plt.xlabel('Stylistic Distance (Cosine)', fontsize=12)
    plt.tight_layout()
    
    plt.savefig(output_filename)
    print(f"Greyscale dendrogram saved to '{output_filename}'")


if __name__ == '__main__':
    # --- Analysis 1: WITHOUT Stop Words ---
    generate_cluster_analysis_greyscale(
        dtm_filepath='dtm_content_words.csv',
        output_filename='cosine_cluster_no_stopwords_greyscale.png',
        plot_title='Cluster Analysis (Content Words Only)'
    )
    
    # --- Analysis 2: WITH Stop Words ---
    generate_cluster_analysis_greyscale(
        dtm_filepath='dtm_all_words.csv',
        output_filename='cosine_cluster_with_stopwords_greyscale.png',
        plot_title='Cluster Analysis (All Words, Including Stop Words)'
    )