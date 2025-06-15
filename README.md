# A Comparative Stylometric Analysis of "Huckleberry Finn" Russian Translations

## Project Objective

This project undertakes a computational stylometric analysis of five different Russian translations of Mark Twain's novel, *The Adventures of Huckleberry Finn*.

The primary goal is a descriptive comparison of the distinct stylistic choices made by each known translator. This analysis is not concerned with authorship attribution or tracking a linear evolution of translation style over time. Instead, it aims to create a "stylistic fingerprint" for each translation, quantitatively highlighting the unique linguistic patterns that differentiate them from one another.

## Datasets

The analysis is based on the following texts:

* **Translations:** Five distinct Russian translations of *The Adventures of Huckleberry Finn*, published between 1911 and 1960.

## Methodology

The core of this project involves using computational linguistic techniques to extract and analyze stylistic features from the translated texts. The workflow is as follows:

1.  **Tokenization and Lemmatization:** All five Russian translations are processed through a standard NLP pipeline. This includes **tokenization** to break the text into individual words and **lemmatization** to normalize words to their base dictionary form. This normalization is crucial for accurately analyzing vocabulary and other lexical features in a morphologically rich language like Russian.
2.  **Feature Extraction:** A set of linguistic features is extracted from each text. These may include, but are not limited to:
    * Vocabulary richness (Type-Token Ratio)
    * Average sentence length and complexity
    * Part-of-speech (POS) tag frequencies
    * Punctuation patterns
    * Frequency of specific function words
3.  **Stylometric Analysis:** Using the extracted features, the translations are compared against one another to quantify their stylistic similarities and differences. This allows for a detailed descriptive analysis of each translator's unique approach to rendering the source material.

## Repository Structure

This repository is organized as follows:

* **/data:** Contains the raw, tokenized, and lemmatized text files for the five translations.
* **/scripts:** Includes reusable scripts for tasks such as data cleaning, text processing, and feature extraction.
* **/notebooks:** Jupyter notebooks used for exploratory data analysis, visualization, and the main stylometric analysis.
* **/results:** Contains the output of the analysis, including data visualizations, tables, and summary reports.
