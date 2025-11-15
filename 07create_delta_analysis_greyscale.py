import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np
import seaborn as sns

def plot_greyscale_distance_heatmap(distance_df: pd.DataFrame, output_filename: str, plot_title: str):
    """
    Creates and saves a GREYSCALE heatmap from a distance matrix DataFrame.
    (Merged from script 09)
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        distance_df,
        annot=True,          # Show the distance scores in each cell
        cmap='Greys',        # Use a greyscale color map
        fmt=".4f",           # Format numbers to 4 decimal places
        linewidths=.5,       # Add lines for clarity
        linecolor='black'
    )
    plt.title(plot_title, fontsize=16)
    plt.tight_layout()
    plt.savefig(output_filename)
    print(f"Greyscale distance heatmap saved to '{output_filename}'")


def generate_delta_cluster_analysis_greyscale(dtm_filepath: str, dendrogram_filename: str, heatmap_filename: str, results_csv_filename: str, plot_title_prefix: str):
    """
    Loads a DTM, calculates pairwise Classic Delta distances, and saves
    the resulting CSV, greyscale dendrogram, and greyscale heatmap.
    """
    print(f"\n--- Running Greyscale Classic Delta Analysis for: {plot_title_prefix} ---")
    
    # Step 1: Load the DTM
    try:
        dtm = pd.read_csv(dtm_filepath, index_col=0)
        print(f"Loaded DTM from '{dtm_filepath}'.")
    except FileNotFoundError:
        print(f"ERROR: File not found at '{dtm_filepath}'.")
        return

    # Step 2: Scale the data to get z-scores
    scaler = StandardScaler()
    z_scores_matrix = scaler.fit_transform(dtm)
    z_scores_df = pd.DataFrame(z_scores_matrix, index=dtm.index, columns=dtm.columns)

    # Step 3: Calculate the pairwise Classic Delta distance matrix
    num_docs = len(z_scores_df)
    delta_dist_matrix = np.zeros((num_docs, num_docs))
    doc_names = z_scores_df.index.tolist()

    for i in range(num_docs):
        for j in range(i + 1, num_docs):
            dist = np.mean(np.abs(z_scores_df.iloc[i] - z_scores_df.iloc[j]))
            delta_dist_matrix[i, j] = dist
            delta_dist_matrix[j, i] = dist

    # Create a labeled DataFrame for the matrix
    delta_df = pd.DataFrame(delta_dist_matrix, index=doc_names, columns=doc_names)
    print("\n--- Classic Delta Distance Matrix ---")
    print(delta_df)
    
    # Save the distance matrix to a CSV file
    delta_df.to_csv(results_csv_filename)
    print(f"Distance matrix saved to '{results_csv_filename}'")
    
    # Call the GREYSCALE heatmap plotting function
    plot_greyscale_distance_heatmap(
        delta_df,
        output_filename=heatmap_filename,
        plot_title=f'Classic Delta Distance Matrix ({plot_title_prefix})'
    )

    # Step 4: Perform Hierarchical Clustering
    condensed_dist_matrix = delta_dist_matrix[np.triu_indices(num_docs, k=1)]
    linkage_matrix = linkage(condensed_dist_matrix, method='ward')

    # Step 5: Create and save the GREYSCALE dendrogram
    plt.figure(figsize=(12, 8))
    dendrogram(
        linkage_matrix,
        labels=doc_names,
        orientation='right',
        leaf_font_size=12,
        # This function forces all branches of the tree to be black (from script 09)
        link_color_func=lambda k: 'black' 
    )
    plt.title(f'Cluster Analysis ({plot_title_prefix}) using Classic Delta', fontsize=16)
    plt.xlabel('Classic Delta Distance 0% Culled', fontsize=12)
    plt.tight_layout()
    plt.savefig(dendrogram_filename)
    print(f"Greyscale dendrogram saved to '{dendrogram_filename}'")


if __name__ == '__main__':
    # --- Analysis 1: WITHOUT Stop Words (Content Words) ---
    generate_delta_cluster_analysis_greyscale(
        dtm_filepath='dtm_content_words.csv',
        dendrogram_filename='delta_cluster_no_stopwords_greyscale.png',
        heatmap_filename='delta_heatmap_no_stopwords_greyscale.png',
        results_csv_filename='delta_results_content_words.csv',
        plot_title_prefix='of Content Words'
    )
    
    # --- Analysis 2: WITH Stop Words (All Words) ---
    generate_delta_cluster_analysis_greyscale(
        dtm_filepath='dtm_all_words.csv',
        dendrogram_filename='delta_cluster_with_stopwords_greyscale.png',
        heatmap_filename='delta_heatmap_with_stopwords_greyscale.png',
        results_csv_filename='delta_results_all_words.csv',
        plot_title_prefix='of All Words'
    )