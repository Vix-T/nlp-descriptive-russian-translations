# A Comparative Stylometric Analysis of "Huckleberry Finn" Russian Translations

## Project Objective

This project undertakes a computational stylometric analysis of five different Russian translations of Mark Twain's novel, *The Adventures of Huckleberry Finn*.
The primary goal is a descriptive comparison of the distinct stylistic choices made by each known translator. This analysis is not concerned with authorship attribution or tracking a linear evolution of translation style over time. Instead, it aims to create a "stylistic fingerprint" for each translation, quantitatively highlighting the unique linguistic patterns that differentiate them from one another.

## Datasets

The analysis is based on the following texts:
* **Translations:** Five distinct Russian translations of *The Adventures of Huckleberry Finn*, published between 1911 and 1960, included in this repository as `Ru1.txt` through `Ru5.txt`.
* **Source:** The English-language text, `En.txt`, is included for reference.

## Methodology: The 26-Step Pipeline

The project workflow is organized into a pipeline of 28 scripts, separated into five distinct phases. The scripts are numbered to be run in logical order.

### Phase 1: Core Data Preparation

**1. `01dataprep_clean_lemmatize.py`**
* **Purpose:** Reads the raw `.txt` files, cleans them (lowercase, removes punctuation/numbers), and lemmatizes the text.
* **Input:** `Ru1.txt`, `Ru2.txt`, ...
* **Output:** `Ru1_clean_lemmatized.txt`, `Ru2_clean_lemmatized.txt`, ...

**2. `02dataprep_removestopwords.py`**
* **Purpose:** Reads the lemmatized files from Step 1 and removes all common Russian stop words.
* **Input:** `Ru1_clean_lemmatized.txt`, `Ru2_clean_lemmatized.txt`, ...
* **Output:** `Ru1_clean_lemmatized_nostops.txt`, `Ru2_clean_lemmatized_nostops.txt`, ...

---

### Phase 2: Feature & Matrix Generation

**3. `03feature_extraction.py`**
* **Purpose:** Gathers a rich set of stylometric features (TTR, entropy, n-gram frequencies, POS counts, etc.) from all text files and saves them to a central `.json` file for each book.
* **Input:** `Ru#.txt`, `Ru#_clean_lemmatized.txt`, `Ru#_clean_lemmatized_nostops.txt`
* **Output:** `Ru1_features.json`, `Ru2_features.json`, ...

**4. `04create_dtm.py`**
* **Purpose:** Creates a Document-Term Matrix (DTM) using only the **content words** (no stop words) for Delta analysis.
* **Input:** `Ru1_clean_lemmatized_nostops.txt`, `Ru2_clean_lemmatized_nostops.txt`, ...
* **Output:** `dtm_content_words.csv`

**5. `05create_dtm_with_stopwords.py`**
* **Purpose:** Creates a DTM using **all words** (including stop words) by reading the pre-calculated frequencies from the `.json` files.
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `dtm_all_words.csv`

**6. `06create_feature_summary.py`**
* **Purpose:** Reads the `.json` feature files and creates a single, high-level summary table (`.csv`) of the main numerical features (TTR, avg. sentence length, etc.).
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `stylometric_summary.csv`

---

### Phase 3: Stylometric & Lexical Analysis

**7. `07create_delta_analysis_greyscale.py`**
* **Purpose:** Performs Burrows' Delta analysis on both DTMs and creates greyscale dendrograms (cluster trees) and heatmaps to visualize the results.
* **Input:** `dtm_content_words.csv`, `dtm_all_words.csv`
* **Output:** `delta_results_...csv`, `delta_cluster_...greyscale.png`, `delta_heatmap_...greyscale.png`

**8. `08pca_matrices_greyscale.py`**
* **Purpose:** Performs Principal Component Analysis (PCA) and Cosine Similarity analysis on both DTMs to create alternative visualizations of text similarity.
* **Input:** `dtm_content_words.csv`, `dtm_all_words.csv`
* **Output:** `pca_analysis_...greyscale.png`, `similarity_heatmap_...greyscale.png`

**9. `09run_spectral_greyscale.py`**
* **Purpose:** Performs Spectral Embedding (another similarity analysis) using TF-IDF vectorization to create a 2D cluster plot.
* **Input:** `Ru1_clean_lemmatized.txt`, `Ru2_clean_lemmatized.txt`, ...
* **Output:** `spectral_embedding_plot_greyscale.png`

**10. `10cosine_cluster_greyscale.py`**
* **Purpose:** Uses Cosine Distance (different from Delta) to perform a cluster analysis and generate greyscale dendrograms.
* **Input:** `dtm_content_words.csv`, `dtm_all_words.csv`
* **Output:** `cosine_cluster_...greyscale.png`

**11. `11mfw_greyscale.py`**
* **Purpose:** Reads the `.json` files and creates 10 greyscale bar charts showing the Top 20 most frequent words (MFW) for each book (with and without stop words).
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `mfw_with_stopwords_...png`, `mfw_no_stopwords_...png` (10 files)

**12. `12create_all_word_comparisons_greyscale.py`**
* **Purpose:** Creates a "Word vs. Text" heatmap to compare the frequency of the Top 30 **all words** (including stop words) across all 5 translations.
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `mfw_all_words_heatmap_greyscale.png`

**13. `13create_content_word_comparisons_greyscale.py`**
* **Purpose:** Creates a "Word vs. Text" heatmap to compare the frequency of the Top **content words** across all 5 translations.
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `mfw_combined_heatmap_greyscale_sorted.png`

**14. `14kw_index.py`**
* **Purpose:** Calculates two advanced lexical richness metrics (Yule's K and Honoré's W) that are not in the main feature set.
* **Input:** `Ru1_clean_lemmatized_nostops.txt`, `Ru2_clean_lemmatized_nostops.txt`, ...
* **Output:** `lexical_diversity_results.csv`

**15. `15create_visualizations_greyscale.py`**
* **Purpose:** Creates the final summary bar charts (TTR, Entropy, and Avg. Sentence Length) from the summary table.
* **Input:** `stylometric_summary.csv`
* **Output:** `ttr_comparison_greyscale_labeled.png`, `sentence_length_comparison_greyscale_labeled.png`

**16. `16create_pos_richness_analysis.py`**
* **Purpose:** Performs a detailed Part-of-Speech (POS) analysis on **Raw** text and TTR/Entropy on **Lemmatized** text, outputting the results as plots and a table image.
* **Input:** `Ru#.txt`, `Ru#_clean_lemmatized_nostops.txt`
* **Output:** `diagnostics/Ru#_pos_distribution.png`, `diagnostics/diagnostic_stats_table.png`

---

### Phase 4: Network Analysis

**17. `17create_mfinder_network.py`**
* **Purpose:** Creates network input files for `mfinder` based on **lemmatized** dataset that still includes stopwords.
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `mfinder-analysis/Ru#_mfinder_input.txt`, `mfinder-analysis/Ru#_word_id_mapping.json`

**18. `18run_mfinder.sh`**
* **Purpose:** Master shell script that runs the *entire* prep pipeline (`01`, `02`, `03`, `17`), then automatically runs the `mfinder` tool on the inputs that have been structured for mfinder.
* **Action:** Runs scripts `01`, `02`, `03`, `17`, then runs `mfinder`.
* **Output:** `mfinder-analysis/Ru#_mfinder_output_OUT.txt`, `mfinder-analysis/Ru#_mfinder_output_MEMBERS.txt`

**19. `19parse_mfinder_results.py`**
* **Purpose:** Reads the numeric `mfinder` results for the mfinder network and translates them back into human-readable word-based reports.
* **Input:** `mfinder-analysis/Ru#_output_MEMBERS.txt`, `mfinder-analysis/Ru#_word_id_mapping.json`
* **Output:** `mfinder-analysis/Ru#_analysis_report.txt`

**20. `20motif_barchart.py`**
* **Purpose:** Creates a greyscale grouped bar chart comparing the normalized Significance Profile (SP) scores of key motifs.
* **Input:** `mfinder-analysis/Ru#_mfinder_output_OUT.txt`
* **Output:** `key_motifs_grouped_bar_greyscale_normalized.png`

**21. `21z-score_heatmap_greyscale.py`**
* **Purpose:** Creates a heatmap of **Raw Z-Scores** to highlight statistical significance (marked with `*` for |Z| > 2.0).
* **Input:** `mfinder-analysis/Ru#_mfinder_output_OUT.txt`
* **Output:** `heatmap_greyscale_significant.png`

**22. `22create_significance_profile.py`**
* **Purpose:** Creates a heatmap of **L2-Normalized Z-Scores** (Significance Profile) to compare the "shape" of the network fingerprints across texts of different sizes.
* **Input:** `mfinder-analysis/Ru#_mfinder_output_OUT.txt`
* **Output:** `heatmap_significance_profile_greyscale.png`

---

### Phase 5: Rankings & Advanced Metrics

**23. `23plot_greyscale_pos_ranks.py`**
* **Purpose:** Creates a heatmap showing the *rank* (1st, 2nd...) of the Top 10 Part-of-Speech tags, allowing for length-independent grammatical comparison.
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `pos_rank_heatmap_greyscale.png`

**24. `24centrality_rankings.py`**
* **Purpose:** Calculates **Betweenness Centrality** on the full mfinder network to identify "Bridge Words" (connectors) and visualizes the Top 20.
* **Input:** `mfinder-analysis/Ru#_mfinder_input.txt`
* **Output:** `mfinder-analysis/Ru#_betweenness_rankings.csv`, `mfinder-analysis/Ru#_betweenness_top20_greyscale.png`

**25. `25plot_greyscale_mfw_ranks.py`**
* **Purpose:** Creates a heatmap showing the *rank* of top content words.
* **Input:** `Ru1_clean_lemmatized_nostops.txt`, `Ru2_clean_lemmatized_nostops.txt`, ...
* **Output:** `mfw_content_words_heatmap_ranked_greyscale.png`

**26. `26plot_betweenness_ranks.py`**
* **Purpose:** Creates a ranked heatmap of the top "Bridge Words" across all translations for direct structural comparison.
* **Input:** `mfinder-analysis/Ru#_betweenness_rankings.csv`
* **Output:** `mfinder-analysis/betweenness_rank_heatmap_greyscale.png`

## Repository Structure

* `Ru#.txt`, `En.txt`: The raw, original source text files.
* `01...` - `26...`: The Python scripts and shell scripts that form the core pipeline, numbered in their logical order.
* `.gitignore`: Specifies all generated files (e.g., `*.csv`, `*.json`, `*.png`, `.venv/`) to be ignored by Git.
* `mfinder-analysis/`: Folder containing all inputs, outputs, and reports for the network analysis.
* `diagnostics/`: Folder containing plot outputs from the POS & richness analysis (script `16`).
* `mfinder_mac/`: The `mfinder` executable.

## How to Run

1.  **Set Up the Environment:**
    * Ensure you have Python 3.9+ installed.
    * Create a virtual environment: `python3 -m venv .venv`
    * Activate it: `source .venv/bin/activate`
    * Install all required libraries:
        ```bash
        pip install pandas numpy scipy scikit-learn matplotlib seaborn nltk pymorphy2 networkx
        ```
    * Download NLTK data (run in an active `venv`):
        ```bash
        python3 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt_tab')"
        ```

2.  **Run the Full Pipeline:**
    The master shell script will run the entire pipeline (Phases 1-4), including all prep steps. You must make it executable first:
    ```bash
    chmod +x 18run_mfinder_mfinder.sh
    ```
    Then, run it:
    ```bash
    ./18run_mfinder_mfinder.sh
    ```

3.  **Run Phase 5 (Advanced Metrics):**
    Run the final ranking scripts individually:
    ```bash
    python 24centrality_rankings.py
    python 26plot_betweenness_ranks.py
    ```
