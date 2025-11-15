import pandas as pd
import json
import os

# Use the same label mapping to keep everything consistent
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def create_dtm_with_stopwords(directory: str = '.') -> pd.DataFrame:
    """
    Creates a Document-Term Matrix from the full unigram frequency data
    (including stop words) in the feature files.

    Args:
        directory (str): The directory containing the '_features.json' files.

    Returns:
        pd.DataFrame: The resulting Document-Term Matrix.
    """
    print("--- Creating Document-Term Matrix (with stop words) ---")
    
    all_word_freqs = {}
    master_word_list = set()

    # Step 1: Read all word frequencies from the JSON files
    for filename in sorted([f for f in os.listdir(directory) if f.endswith('_features.json')]):
        book_name = filename.split('_features.json')[0]
        new_label = label_mapping.get(book_name, book_name)

        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Use 'unigram_frequencies' which includes all words
        unigram_data = data.get('unigram_frequencies')
        if not unigram_data:
            print(f"No unigram frequency data found for {book_name}. Skipping.")
            continue
        
        all_word_freqs[new_label] = unigram_data
        master_word_list.update(unigram_data.keys())
        
    if not all_word_freqs:
        print("No feature files found or parsed. Cannot create DTM.")
        return pd.DataFrame()

    print(f"Found a total of {len(master_word_list)} unique words across all documents.")

    # Step 2: Create and populate the DataFrame (DTM)
    dtm = pd.DataFrame(all_word_freqs, index=sorted(list(master_word_list))).T

    # Step 3: Fill any missing values with 0
    dtm = dtm.fillna(0).astype(int)

    return dtm

if __name__ == '__main__':
    document_term_matrix = create_dtm_with_stopwords()
    
    if not document_term_matrix.empty:
        output_filename = 'dtm_all_words.csv'
        document_term_matrix.to_csv(output_filename)
        
        print("\n--- DTM with Stop Words (First 5 Rows & 10 Columns) ---")
        print(document_term_matrix.iloc[:5, :10])
        print(f"\nDTM with stop words saved to '{output_filename}'")