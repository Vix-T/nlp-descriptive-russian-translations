import pandas as pd
# StandardScaler is no longer needed in this version
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

def generate_old_pca_and_similarity(dtm_filepath: str, pca_plot_filename: str, plot_title_prefix: str):
    """
    Loads a DTM and performs PCA directly on the unscaled data to replicate
    the older version of the analysis.
    """
    print(f"\n--- Running OLDER Version of Analysis for: {plot_title_prefix} ---")
    
    # Step 1: Load the Document-Term Matrix
    try:
        dtm = pd.read_csv(dtm_filepath, index_col=0)
        print(f"✅ Loaded DTM from '{dtm_filepath}'.")
    except FileNotFoundError:
        print(f"❌ ERROR: File not found at '{dtm_filepath}'.")
        return

    # --- PCA Calculation and Visualization (on UN SCALED data) ---

    # NOTE: The StandardScaler step has been removed.
    # We are passing the raw 'dtm' directly to the PCA function.
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(dtm)
    
    pca_df = pd.DataFrame(data=principal_components, 
                          columns=['Principal Component 1', 'Principal Component 2'], 
                          index=dtm.index)

    # Create the color PCA scatter plot
    plt.figure(figsize=(10, 8))
    sns.scatterplot(x='Principal Component 1', y='Principal Component 2', data=pca_df, s=150)

    # Add red labels to each point
    for i in range(pca_df.shape[0]):
        plt.text(x=pca_df['Principal Component 1'][i]+0.3,
                 y=pca_df['Principal Component 2'][i]+0.3,
                 s=pca_df.index[i],
                 fontdict=dict(color='red', size=10))

    plt.title(f'PCA of Translations ({plot_title_prefix}) - Unscaled', fontsize=16)
    plt.xlabel(f"PC 1 ({pca.explained_variance_ratio_[0]:.1%} Variance)", fontsize=12)
    plt.ylabel(f"PC 2 ({pca.explained_variance_ratio_[1]:.1%} Variance)", fontsize=12)
    plt.axhline(0, color='grey', linestyle='--')
    plt.axvline(0, color='grey', linestyle='--')
    plt.grid()
    plt.savefig(pca_plot_filename)
    print(f"✅ PCA plot (unscaled) saved to '{pca_plot_filename}'")


if __name__ == '__main__':
    # We will just run the analysis on the content words (no stopwords)
    # as that is what your original screenshot showed.
    generate_old_pca_and_similarity(
        dtm_filepath='document_term_matrix.csv',
        pca_plot_filename='pca_analysis_no_stopwords_UNSCALED.png',
        plot_title_prefix='Content Words Only'
    )