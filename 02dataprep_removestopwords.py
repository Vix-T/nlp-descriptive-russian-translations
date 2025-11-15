import os
import nltk
from nltk.corpus import stopwords

#
# Script 2: Stop Word Removal
#
# This script is designed to be run AFTER 01dataprep_clean_lemmatize.py.
# INPUT:  Ru#_clean_lemmatized.txt
# OUTPUT: Ru#_clean_lemmatized_nostops.txt
#

def read_lemmatized_file(file_path: str) -> list:
    """
    Reads a _clean_lemmatized.txt file (which is one long line of tokens)
    and splits it into a list of words.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"Reading: {os.path.basename(file_path)}...")
            # Read the single line of text and split it by spaces
            words = file.read().split() 
            return words
    except FileNotFoundError:
        print(f"ERROR: The file was not found at '{file_path}'")
        return []

def remove_stopwords(word_list: list) -> list:
    """Removes Russian stop words from a list of tokens."""
    print("Removing stop words...")
    
    # Ensure stopwords are downloaded
    try:
        russian_stopwords = set(stopwords.words("russian"))
    except LookupError:
        print("Russian stopwords not found. Downloading...")
        nltk.download('stopwords')
        russian_stopwords = set(stopwords.words("russian"))
    
    # Use a set for faster lookup (good practice)
    tokens_without_stopwords = [word for word in word_list if word not in russian_stopwords]
    
    print(f"   Original tokens: {len(word_list)}")
    print(f"   Tokens after removal: {len(tokens_without_stopwords)}")
    return tokens_without_stopwords

def save_output_text(output_path: str, tokens: list):
    """Saves a list of tokens to a text file, joined by spaces."""
    try:
        final_text = ' '.join(tokens)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(final_text)
        print(f"Successfully saved new file to {os.path.basename(output_path)}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

# --- Main processing loop ---
if __name__ == '__main__':
    
    # --- This list is updated to match your new input filenames ---
    input_files = [
        'Ru1_clean_lemmatized.txt', 
        'Ru2_clean_lemmatized.txt', 
        'Ru3_clean_lemmatized.txt', 
        'Ru4_clean_lemmatized.txt', 
        'Ru5_clean_lemmatized.txt'
    ]
    
    print("--- Starting Stop Word Removal Process ---")
    
    for filename in input_files:
        print(f"\nProcessing {filename}...")
        
        # 1. Read the already-lemmatized tokens from Script 1's output
        lemmatized_tokens = read_lemmatized_file(filename)
        
        if lemmatized_tokens:
            # 2. Remove stop words
            final_tokens = remove_stopwords(lemmatized_tokens)
            
            # 3. Create the new output filename and save
            # --- This logic is updated to match your new output names ---
            output_filename = filename.replace(
                '_clean_lemmatized.txt', 
                '_clean_lemmatized_nostops.txt'
            )
            save_output_text(output_filename, final_tokens)
            
    print("\n--- All files processed successfully! ---")