import pandas as pd
from collections import Counter
import os

# Use the same label mapping to keep everything consistent
label_mapping = {
    'Ru1': 'Ru-1911-Engelgardt',
    'Ru2': 'Ru-1926-Anon',
    'Ru3': 'Ru-1933-Chukovsky-(Ed.)',
    'Ru4': 'Ru-1949-Braude',
    'Ru5': 'Ru-1960-Daruzes'
}

def create_correct_dtm_without_stopwords(directory: str = '.') -> pd.DataFrame:
    """
    Creates a CORRECT Document-Term Matrix from the full content word lists
    in the '*_clean_nostops.txt' files.

    Args:
        directory (str): The directory containing the text files.

    Returns:
        pd.DataFrame: The resulting Document-Term Matrix.
    """
    print("--- Creating CORRECTED Document-Term Matrix (without stop words) ---")
    
    all_word_freqs = {}

    # Find and process the correct source files
    for i in range(1, 6):
        book_name = f"Ru{i}"
        filename = f"{book_name}_clean_nostops.txt"
        file_path = os.path.join(directory, filename)
        
        new_label = label_mapping.get(book_name, book_name)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tokens = f.read().split()
            
            # Get the frequency counts for this document
            all_word_freqs[new_label] = Counter(tokens)
            print(f"✅ Processed {filename} with {len(tokens)} total content words.")

        except FileNotFoundError:
            print(f"❌ ERROR: Source file not found: {filename}")
            continue
            
    if not all_word_freqs:
        print("❌ No source files found. Cannot create DTM.")
        return pd.DataFrame()

    # Create the DataFrame (DTM) from the collected frequency counts
    dtm = pd.DataFrame(all_word_freqs).T

    # Fill any missing values with 0
    dtm = dtm.fillna(0).astype(int)

    return dtm

if __name__ == '__main__':
    # This will create the new, correct DTM
    document_term_matrix = create_correct_dtm_without_stopwords()
    
    if not document_term_matrix.empty:
        # Overwrite the old, flawed DTM file
        document_term_matrix.to_csv('document_term_matrix.csv')
        
        print("\n--- Corrected Document-Term Matrix (First 5 Rows & 10 Columns) ---")
        print(document_term_matrix.iloc[:5, :10])
        print("\n✅ CORRECTED Document-Term Matrix saved to 'document_term_matrix.csv'")