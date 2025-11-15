# A Comparative Stylometric Analysis of "Huckleberry Finn" Russian Translations

## Project Objective

This project undertakes a computational stylometric analysis of five different Russian translations of Mark Twain's novel, *The Adventures of Huckleberry Finn*.
The primary goal is a descriptive comparison of the distinct stylistic choices made by each known translator. This analysis is not concerned with authorship attribution or tracking a linear evolution of translation style over time. Instead, it aims to create a "stylistic fingerprint" for each translation, quantitatively highlighting the unique linguistic patterns that differentiate them from one another.

## Datasets

The analysis is based on the following texts:
* **Translations:** Five distinct Russian translations of *The Adventures of Huckleberry Finn*, published between 1911 and 1960, included in this repository as `Ru1.txt` through `Ru5.txt`.
* **Source:** The English-language text, `En.txt`, is included for reference.

## Project Workflow

This project is organized into a pipeline of 25 scripts, separated into four distinct phases. The scripts are numbered to be run in logical order.


1.  **Phase 1: Core Data Preparation (`01`-`02`)**
    This phase ingests the raw `.txt` files and produces two foundational datasets: one that is cleaned and lemmatized (`..._clean_lemmatized.txt`), and one that also has all stop words removed (`..._clean_lemmatized_nostops.txt`).

2.  **Phase 2: Feature & Matrix Generation (`03`-`06`)**
    This phase converts the clean texts into numerical data. It generates rich `.json` files containing all features (TTR, n-grams, POS counts, etc.) and builds the core Document-Term Matrices (DTMs) for both "content words" and "all words".

3.  **Phase 3: Stylometric & Lexical Analysis (`07`-`17`)**
    This is the main analysis phase. These scripts consume the DTMs and `.json` files to perform a wide range of stylometric tests, including Burrows' Delta, PCA, Cosine Similarity, Spectral Embedding, and lexical richness (Yule's K, Honoré's W). All visualizations are generated in greyscale for publication.

4.  **Phase 4: Network Analysis (`18`-`25`)**
    This phase performs an advanced motif analysis using the `mfinder` tool. It builds two separate networks—a "conceptual" network from lemmatized text and a "syntactic" network from unlemmatized text—and then runs `mfinder`, parses the results, and generates final heatmaps and bar charts of the network Z-scores.

## Repository Structure

* `Ru#.txt`: The five raw Russian translation text files.
* `01...py` - `25...py`: The core Python scripts of the pipeline, numbered in execution order.
* `*.sh`: Two master shell scripts (`20...` and `21...`) that can run the entire mfinder pipeline from start to finish.
* `.gitignore`: Specifies all generated files (e.g., `*.csv`, `*.json`, `*.png`, `.venv/`) to be ignored by Git.
* `conceptual-analysis/`: Contains all inputs, outputs, and reports for the conceptual network analysis.
* `syntactic-analysis/`: Contains all inputs, outputs, and reports for the syntactic network analysis.
* `diagnostics/`: Contains plot outputs from the POS & richness analysis (script `16`).
* `mfinder_mac/`: The `mfinder` executable (ignored by this README's author, but present in user's repo).

## How to Run

1.  **Set Up the Environment:**
    * Ensure you have Python 3.9+ installed.
    * Create a virtual environment: `python3 -m venv .venv`
    * Activate it: `source .venv/bin/activate`
    * Install all required libraries:
        ```bash
        pip install -r requirements.txt 
        # (If no requirements.txt, run: pip install pandas numpy scipy scikit-learn matplotlib seaborn nltk pymorphy2)
        ```

2.  **Run the Full mfinder Analysis:**
    The two master shell scripts will run the entire Phase 4 pipeline (including all necessary prep steps from Phases 1-2).
    * Run `bash 20run_syntactic_mfinder.sh`
    * Run `bash 21run_conceptual_mfinder.sh`

3.  **Run Other Analyses:**
    All other scripts from Phase 3 (e.g., `07create_delta_analysis_greyscale.py`) can be run individually, as long as their prerequisite files (from Phases 1 & 2) exist.
