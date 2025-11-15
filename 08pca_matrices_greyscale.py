import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

def plot_similarity_heatmap_greyscale(similarity_df: pd.DataFrame, output_filename: str, plot_title: str):
    """
    Creates and saves a GREYSCALE heatmap from a similarity matrix DataFrame.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        similarity_df,
        annot=True,          # Show the similarity scores in each cell
        cmap='Greys',        # Use the greyscale color map
        fmt=".4f",           # Format numbers to 4 decimal places
        linewidths=.5,
        linecolor='black'
    )
    plt.title(plot_title, fontsize=16)
    plt.tight_layout()
    plt.savefig(output_filename)
    print(f"Greyscale similarity heatmap saved to '{output_filename}'")

def generate_pca_and_similarity_greyscale(dtm_filepath: str, pca_plot_filename: str, heatmap_filename: str, plot_title_prefix: str):
    """
    Loads a DTM, performs PCA and Cosine Similarity, and saves GREYSCALE plots.
    """
    print(f"\n--- Running Greyscale Analysis for: {plot_title_prefix} ---")
    
    # Step 1: Load the DTM
    try:
        dtm = pd.read_csv(dtm_filepath, index_col=0)
        print(f"Loaded DTM from '{dtm_filepath}'.")
    except FileNotFoundError:
        print(f"ERROR: File not found at '{dtm_filepath}'.")
        return

    # --- PCA Calculation and Greyscale Visualization ---
    scaled_dtm = StandardScaler().fit_transform(dtm)
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(scaled_dtm)
    pca_df = pd.DataFrame(data=principal_components, 
                          columns=['Principal Component 1', 'Principal Component 2'], 
                          index=dtm.index)

    plt.figure(figsize=(10, 8))
    # Create the scatter plot with black points
    sns.scatterplot(x='Principal Component 1', y='Principal Component 2', data=pca_df, s=150, color='black', marker='D')
    # Add black text labels
    for i in range(pca_df.shape[0]):
        plt.text(x=pca_df['Principal Component 1'][i] + 0.1,
                 y=pca_df['Principal Component 2'][i] + 0.1,
                 s=pca_df.index[i],
                 fontdict=dict(color='black', size=10))

    plt.title(f'PCA of Translations ({plot_title_prefix})', fontsize=16)
    plt.xlabel(f"PC 1 ({pca.explained_variance_ratio_[0]:.1%} Variance)", fontsize=12)
    plt.ylabel(f"PC 2 ({pca.explained_variance_ratio_[1]:.1%} Variance)", fontsize=12)
    plt.axhline(0, color='grey', linestyle='--')
    plt.axvline(0, color='grey', linestyle='--')
    plt.grid()
    plt.savefig(pca_plot_filename)
    print(f"Greyscale PCA plot saved to '{pca_plot_filename}'")
    
    # --- Cosine Similarity Matrix and Greyscale Heatmap ---
    similarity_matrix = cosine_similarity(dtm)
    similarity_df = pd.DataFrame(similarity_matrix, 
                                 index=dtm.index, 
                                 columns=dtm.index)
                                 
    print(f"\n--- Cosine Similarity Matrix ({plot_title_prefix}) ---")
    print(similarity_df)
    
    # Call the new greyscale heatmap function
    plot_similarity_heatmap_greyscale(
        similarity_df,
        output_filename=heatmap_filename,
        plot_title=f'Cosine Similarity Matrix ({plot_title_prefix})'
    )

if __name__ == '__main__':
    # --- Analysis 1: WITHOUT Stop Words ---
    generate_pca_and_similarity_greyscale(
        # --- FIXED: Using correct input file from our pipeline ---
        dtm_filepath='dtm_content_words.csv',
        pca_plot_filename='pca_analysis_no_stopwords_greyscale.png',
        heatmap_filename='similarity_heatmap_no_stopwords_greyscale.png',
        plot_title_prefix='Content Words Only'
    )
    
    # --- Analysis 2: WITH Stop Words ---
    generate_pca_and_similarity_greyscale(
        # --- FIXED: Using correct input file from our pipeline ---
        dtm_filepath='dtm_all_words.csv',
        pca_plot_filename='pca_analysis_with_stopwords_greyscale.png',
        heatmap_filename='similarity_heatmap_with_stopwords_greyscale.png',
        plot_title_prefix='All Words, Including Stop Words'
    )