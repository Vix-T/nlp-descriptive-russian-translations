# A Comparative Stylometric Analysis of "Huckleberry Finn" Russian Translations

## Project Objective

This project undertakes a computational stylometric analysis of five different Russian translations of Mark Twain's novel, *The Adventures of Huckleberry Finn*.
The primary goal is a descriptive comparison of the distinct stylistic choices made by each known translator. This analysis is not concerned with authorship attribution or tracking a linear evolution of translation style over time. Instead, it aims to create a "stylistic fingerprint" for each translation, quantitatively highlighting the unique linguistic patterns that differentiate them from one another.

## Datasets

The analysis is based on the following texts:
* **Translations:** Five distinct Russian translations of *The Adventures of Huckleberry Finn*, published between 1911 and 1960, included in this repository as `Ru1.txt` through `Ru5.txt`.
* **Source:** The English-language text, `En.txt`, is included for reference.

## Methodology: The 25-Step Pipeline

The project workflow is organized into a pipeline of 25 scripts, separated into four distinct phases. The scripts are numbered to be run in logical order.

### Phase 1: Core Data Preparation

**1. `01dataprep_clean_lemmatize`**
* **Purpose:** Reads the raw `.txt` files, cleans them (lowercase, removes punctuation/numbers), and lemmatizes the text.
* **Input:** `Ru1.txt`, `Ru2.txt`, ...
* **Output:** `Ru1_clean_lemmatized.txt`, `Ru2_clean_lemmatized.txt`, ...

**2. `02dataprep_removestopwords`**
* **Purpose:** Reads the lemmatized files from Step 1 and removes all common Russian stop words.
* **Input:** `Ru1_clean_lemmatized.txt`, `Ru2_clean_lemmatized.txt`, ...
* **Output:** `Ru1_clean_lemmatized_nostops.txt`, `Ru2_clean_lemmatized_nostops.txt`, ...

---

### Phase 2: Feature & Matrix Generation

**3. `03feature_extraction`**
* **Purpose:** Gathers a rich set of stylometric features (TTR, entropy, n-gram frequencies, POS counts, etc.) from all text files and saves them to a central `.json` file for each book.
* **Input:** `Ru#.txt`, `Ru#_clean_lemmatized.txt`, `Ru#_clean_lemmatized_nostops.txt`
* **Output:** `Ru1_features.json`, `Ru2_features.json`, ...

**4. `04create_dtm`**
* **Purpose:** Creates a Document-Term Matrix (DTM) using only the **content words** (no stop words) for Delta analysis.
* **Input:** `Ru1_clean_lemmatized_nostops.txt`, `Ru2_clean_lemmatized_nostops.txt`, ...
* **Output:** `dtm_content_words.csv`

**5. `05create_dtm_with_stopwords`**
* **Purpose:** Creates a DTM using **all words** (including stop words) by reading the pre-calculated frequencies from the `.json` files.
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `dtm_all_words.csv`

**6. `07create_feature_summary`**
* **Purpose:** Reads the `.json` feature files and creates a single, high-level summary table (`.csv`) of the main numerical features (TTR, avg. sentence length, etc.).
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `stylometric_summary.csv`

---

### Phase 3: Stylometric & Lexical Analysis

**7. `08create_delta_analysis_greyscale`**
* **Purpose:** Performs Burrows' Delta analysis on both DTMs and creates greyscale dendrograms (cluster trees) and heatmaps to visualize the results.
* **Input:** `dtm_content_words.csv`, `dtm_all_words.csv`
* **Output:** `delta_results_...csv`, `delta_cluster_...greyscale.png`, `delta_heatmap_...greyscale.png`

**8. `09pca_matrices_greyscale`**
* **Purpose:** Performs Principal Component Analysis (PCA) and Cosine Similarity analysis on both DTMs to create alternative visualizations of text similarity.
* **Input:** `dtm_content_words.csv`, `dtm_all_words.csv`
* **Output:** `pca_analysis_...greyscale.png`, `similarity_heatmap_...greyscale.png`

**9. `10run_spectral_greyscale`**
* **Purpose:** Performs Spectral Embedding (another similarity analysis) using TF-IDF vectorization to create a 2D cluster plot.
* **Input:** `Ru1_clean_lemmatized.txt`, `Ru2_clean_lemmatized.txt`, ...
* **Output:** `spectral_embedding_plot_greyscale.png`

**10. `11cosine_cluster_greyscale`**
* **Purpose:** Uses Cosine Distance (different from Delta) to perform a cluster analysis and generate greyscale dendrograms.
* **Input:** `dtm_content_words.csv`, `dtm_all_words.csv`
* **Output:** `cosine_cluster_...greyscale.png`

**11. `12mfw_greyscale`**
* **Purpose:** Reads the `.json` files and creates 10 greyscale bar charts showing the Top 20 most frequent words (MFW) for each book (with and without stop words).
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `mfw_with_stopwords_...png`, `mfw_no_stopwords_...png` (10 files)

**12. `13create_all_word_comparisons_greyscale`**
* **Purpose:** Creates a "Word vs. Text" heatmap to compare the frequency of the Top 30 **all words** (including stop words) across all 5 translations.
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `mfw_all_words_heatmap_greyscale.png`

**13. `14create_content_word_comparisons_greyscale`**
* **Purpose:** Creates a "Word vs. Text" heatmap to compare the frequency of the Top **content words** across all 5 translations.
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `mfw_combined_heatmap_greyscale_sorted.png`

**14. `15kw_index`**
* **Purpose:** Calculates two advanced lexical richness metrics (Yule's K and Honoré's W) that are not in the main feature set.
* **Input:** `Ru1_clean_lemmatized_nostops.txt`, `Ru2_clean_lemmatized_nostops.txt`, ...
* **Output:** `lexical_diversity_results.csv`

**15. `16create_visualizations_greyscale`**
* **Purpose:** Creates the final summary bar charts (TTR and Avg. Sentence Length) from the summary table.
* **Input:** `stylometric_summary.csv`
* **Output:** `ttr_comparison_greyscale_labeled.png`, `sentence_length_comparison_greyscale_labeled.png`

**16. `17create_pos_richness_analysis`**
* **Purpose:** Performs a detailed Part-of-Speech (POS) analysis and also calculates TTR/Entropy, outputting the results as plots and a table image.
* **Input:** `Ru#_clean_lemmatized.txt`, `Ru#_clean_lemmatized_nostops.txt`
* **Output:** `diagnostics/Ru#_pos_distribution.png`, `diagnostics/diagnostic_stats_table.png`

**17. `26plot_greyscale_mfw_ranks`**
* **Purpose:** Creates a "Word vs. Text" heatmap showing the *rank* (1st, 2nd, 3rd...) of top content words, rather than their raw frequency.
* **Input:** `Ru1_clean_lemmatized_nostops.txt`, `Ru2_clean_lemmatized_nostops.txt`, ...
* **Output:** `mfw_content_words_heatmap_ranked_greyscale.png`

---

### Phase 4: Network Analysis (mfinder Pipeline)

**18. `17create_conceptual_network`**
* **Purpose:** Creates network input files for `mfinder` based on **lemmatized** bigrams (a "conceptual" network).
* **Input:** `Ru1_features.json`, `Ru2_features.json`, ...
* **Output:** `conceptual-analysis/Ru#_mfinder_input.txt`, `conceptual-analysis/Ru#_word_id_mapping.json`

**19. `18create_syntactic_network`**
* **Purpose:** Creates network input files for `mfinder` based on **unlemmatized** bigrams (a "syntactic" network).
* **Input:** `Ru1.txt`, `Ru2.txt`, ...
* **Output:** `syntactic-analysis/Ru#_syntactic_input.txt`, `syntactic-analysis/Ru#_syntactic_mapping.json`

**20. `19run_conceptual_mfinder.sh`**
* **Purpose:** Master script that runs the *entire* prep pipeline (`01`, `02`, `03`, `17`), then automatically runs `mfinder` on the conceptual inputs.
* **Action:** Runs scripts `01`, `02`, `03`, `17`, then runs `mfinder`.
* **Output:** `conceptual-analysis/Ru#_conceptual_output_OUT.txt`, `conceptual-analysis/Ru#_conceptual_output_MEMBERS.txt`

**21. `20run_syntactic_mfinder.sh`**
* **Purpose:** Master script that runs `18create_syntactic_network`, then automatically runs the `mfinder` tool on all of its outputs.
* **Action:** Runs script `18`, then runs `mfinder`.
* **Output:** `syntactic-analysis/Ru#_syntactic_output_OUT.txt`, `syntactic-analysis/Ru#_syntactic_output_MEMBERS.txt`

**22. `22parse_mfinder_results_syntactic`**
* **Purpose:** Reads the numeric `mfinder` results for the **syntactic** network and translates them back into human-readable word-based reports.
* **Input:** `syntactic-analysis/Ru#_syntactic_output_MEMBERS.txt`, `syntactic-analysis/Ru#_syntactic_mapping.json`
* **Output:** `syntactic-analysis/Ru#_syntactic_analysis_report.txt`

**23. `23parse_mfinder_results_conceptual`**
* **Purpose:** Reads the numeric `mfinder` results for the **conceptual** network and translates them back into human-readable word-based reports.
* **Input:** `conceptual-analysis/Ru#_conceptual_output_MEMBERS.txt`, `conceptual-analysis/Ru#_word_id_mapping.json`
* **Output:** `conceptual-analysis/Ru#_conceptual_analysis_report.txt`

**24. `24motif_barchart`**
* **Purpose:** Creates a greyscale grouped bar chart comparing the Z-scores (significance) of key motifs from the **syntactic** network.
* **Input:** `syntactic-analysis/Ru#_syntactic_output_OUT.txt`
* **Output:** `key_motifs_grouped_bar_greyscale.png`

**25. `25z-score_heatmap_greyscale`**
* **Purpose:** Creates a comprehensive greyscale heatmap of the Z-scores for *all* motifs from the **syntactic** network.
* **Input:** `syntactic-analysis/Ru#_syntactic_output_OUT.txt`
* **Output:** `heatmap_greyscale_significant.png`

## Repository Structure

* `Ru#.txt`, `En.txt`: The raw, original source text files.
* `01...` - `25...`: The Python scripts and shell scripts that form the core pipeline, numbered in their logical order.
* `.gitignore`: Specifies all generated files (e.g., `*.csv`, `*.json`, `*.png`, `.venv/`) to be ignored by Git.
* `conceptual-analysis/`: Folder containing all inputs, outputs, and reports for the conceptual network analysis.
* `syntactic-analysis/`: Folder containing all inputs, outputs, and reports for the syntactic network analysis.
* `diagnostics/`: Folder containing plot outputs from the POS & richness analysis (script `16`).
* `mfinder_mac/`: The `mfinder` executable.

## How to Run

1.  **Set Up the Environment:**
    * Ensure you have Python 3.9+ installed.
    * Create a virtual environment: `python3 -m venv .venv`
    * Activate it: `source .venv/bin/activate`
    * Install all required libraries:
        ```bash
        pip install pandas numpy scipy scikit-learn matplotlib seaborn nltk pymorphy2
        ```
    * Download NLTK data (run in an active `venv`):
        ```bash
        python3 -c "import nltk; nltk.download('stopwords'); nltk.download('punkt_tab')"
        ```

2.  **Run the Full mfinder Analysis:**
    The two master shell scripts will run the entire Phase 4 pipeline, including all necessary prep steps. You must make them executable first:
    ```bash
    chmod +x 19run_conceptual_mfinder.sh
    chmod +x 20run_syntactic_mfinder.sh
    ```
    Then, run them:
    ```bash
    ./19run_conceptual_mfinder.sh
    ./20run_syntactic_mfinder.sh
    ```

3.  **Run Other Analyses:**
    All other scripts (e.g., `07create_delta_analysis_greyscale`) can be run individually, as long as their prerequisite files (from Phases 1 & 2) exist.
    ```bash
    python 07create_delta_analysis_greyscale
    ```
