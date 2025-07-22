import re
import pymorphy2
import os # Import the os module to handle file paths

#
# Scripts to prepare text data for analysis.
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

def clean_text(text: str) -> str:
    """Converts text to lowercase and removes punctuation and numbers."""
    text = text.lower()
    text = re.sub(r'[^а-я\s]', '', text)
    return text

def lemmatize_text(text: str) -> list:
    """Tokenizes and lemmatizes the text."""
    words = text.split()
    morph = pymorphy2.MorphAnalyzer()
    lemmas = [morph.parse(word)[0].normal_form for word in words]
    return lemmas

def save_cleaned_text(output_path: str, tokens: list):
    """
    Saves a list of tokens to a text file, joined by spaces.
    
    Args:
        output_path (str): The path for the new output file.
        tokens (list): The list of cleaned and lemmatized words.
    """
    try:
        # Join the list of tokens back into a single string with spaces
        final_text = ' '.join(tokens)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(final_text)
        print(f"💾 Successfully saved cleaned text to {os.path.basename(output_path)}")
    except Exception as e:
        print(f"❌ An error occurred while saving the file: {e}")

# --- Main processing loop ---
if __name__ == '__main__':
    # List of files to process
    input_files = ['Ru1.txt', 'Ru2.txt', 'Ru3.txt', 'Ru4.txt', 'Ru5.txt']
    
    print("--- Starting Batch Processing ---")
    
    # Loop through each file in the list
    for filename in input_files:
        print(f"\nProcessing {filename}...")
        
        # 1. Parse the file
        book_text = parse_text_file(filename)
        
        # 2. Proceed only if the file was read successfully
        if book_text:
            # 3. Clean the text
            cleaned_book_text = clean_text(book_text)
            
            # 4. Lemmatize the cleaned text
            lemmatized_tokens = lemmatize_text(cleaned_book_text)
            
            # 5. Define the output filename and save the result
            output_filename = filename.replace('.txt', '_clean.txt')
            save_cleaned_text(output_filename, lemmatized_tokens)
            
    print("\n--- All files processed successfully! ---")