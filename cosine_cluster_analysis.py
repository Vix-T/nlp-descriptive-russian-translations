import pandas as pd
from sklearn.metrics.pairwise import cosine_distances
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

def generate_cluster_analysis(dtm_filepath: str, output_filename: str, plot_title: str):
    """
    Loads a Document-Term Matrix, performs a Cluster Analysis,
    and saves the resulting dendrogram.

    Args:
        dtm_filepath (str): The path to the DTM csv file.
        output_filename (str): The filename for the output plot image.
        plot_title (str): The title for the plot.
    """
    print(f"\n--- Running Cluster Analysis for: {plot_title} ---")
    
    # Step 1: Load the Document-Term Matrix
    try:
        dtm = pd.read_csv(dtm_filepath, index_col=0)
        print(f"✅ Loaded DTM from '{dtm_filepath}' with {dtm.shape[0]} documents and {dtm.shape[1]} terms.")
    except FileNotFoundError:
        print(f"❌ ERROR: File not found at '{dtm_filepath}'. Please create the DTM first.")
        return

    # Step 2: Calculate the stylistic distance between documents.
    # We will use Cosine Distance, which is excellent for text analysis.
    # The result is a square matrix showing the distance between each pair of texts.
    dist_matrix = cosine_distances(dtm)
    
    # Step 3: Perform Hierarchical Clustering using a linkage method.
    # 'ward' is a good default method that tends to create well-defined clusters.
    linkage_matrix = linkage(dist_matrix, method='ward')

    # Step 4: Create and save the dendrogram visualization
    plt.figure(figsize=(12, 8))
    dendrogram(
        linkage_matrix,
        labels=dtm.index.tolist(),
        orientation='right',
        leaf_font_size=12
    )

    plt.title(plot_title, fontsize=16)
    plt.xlabel('Stylistic Distance (Cosine)', fontsize=12)
    plt.tight_layout() # Adjust plot to prevent labels from being cut off
    
    plt.savefig(output_filename)
    print(f"✅ Dendrogram saved to '{output_filename}'")


if __name__ == '__main__':
    # --- Analysis 1: WITHOUT Stop Words ---
    # This analysis focuses on the author's choice of content words.
    generate_cluster_analysis(
        dtm_filepath='document_term_matrix.csv',
        output_filename='cluster_analysis_no_stopwords.png',
        plot_title='Cluster Analysis (Content Words Only)'
    )
    
    # --- Analysis 2: WITH Stop Words ---
    # This analysis focuses on function words and overall structure.
    generate_cluster_analysis(
        dtm_filepath='document_term_matrix_with_stops.csv',
        output_filename='cluster_analysis_with_stopwords.png',
        plot_title='Cluster Analysis (All Words, Including Stop Words)'
    )