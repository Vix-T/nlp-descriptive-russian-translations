import re
import pymorphy2
import os
import nltk
from nltk.corpus import stopwords

#
# Scripts to prepare text data, including stop word removal.
#

def parse_text_file(file_path: str) -> str:
    """Reads a text file and returns its contents as a single string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            print(f"📄 Reading {os.path.basename(file_path)}...")
            return file.read()
    except FileNotFoundError:
        print(f"❌ ERROR: The file was not found at '{file_path}'")
        return ""

def clean_and_process_text(text: str) -> list:
    """
    Cleans, tokenizes, lemmatizes, and removes stop words from text.
    
    Returns:
        list: A list of processed words (tokens).
    """
    # 1. Clean text (lowercase, remove punctuation/numbers)
    text = text.lower()
    text = re.sub(r'[^а-я\s]', '', text)
    
    # 2. Tokenize (split into words)
    words = text.split()
    
    # 3. Lemmatize words
    morph = pymorphy2.MorphAnalyzer()
    lemmas = [morph.parse(word)[0].normal_form for word in words]
    
    # 4. Remove stop words
    russian_stopwords = stopwords.words("russian")
    lemmas_without_stopwords = [word for word in lemmas if word not in russian_stopwords]
    print(f"🚫 Removed stop words.")
    
    return lemmas_without_stopwords

def save_cleaned_text(output_path: str, tokens: list):
    """Saves a list of tokens to a text file, joined by spaces."""
    try:
        final_text = ' '.join(tokens)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(final_text)
        print(f"💾 Successfully saved cleaned text to {os.path.basename(output_path)}")
    except Exception as e:
        print(f"❌ An error occurred while saving the file: {e}")

# --- Main processing loop ---
if __name__ == '__main__':
    # List of original files to process
    input_files = ['Ru1.txt', 'Ru2.txt', 'Ru3.txt', 'Ru4.txt', 'Ru5.txt']
    
    print("--- Starting Batch Processing (with Stop Word Removal) ---")
    
    for filename in input_files:
        print(f"\nProcessing {filename}...")
        
        book_text = parse_text_file(filename)
        
        if book_text:
            processed_tokens = clean_and_process_text(book_text)
            
            # Create a new output filename to reflect stop word removal
            output_filename = filename.replace('.txt', '_clean_nostops.txt')
            save_cleaned_text(output_filename, processed_tokens)
            
    print("\n--- All files processed successfully! ---")