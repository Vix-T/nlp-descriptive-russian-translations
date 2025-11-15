import pandas as pd
import json
import os

def load_features_to_dataframe(directory: str = '.') -> pd.DataFrame:
    """
    Finds all '*_features.json' files in a directory, loads them,
    and compiles them into a single pandas DataFrame.

    Args:
        directory (str): The directory where the JSON files are located.

    Returns:
        pd.DataFrame: A DataFrame containing the features for all books.
    """
    all_features_list = []
    
    # Find all feature files in the current directory
    for filename in os.listdir(directory):
        if filename.endswith('_features.json'):
            # Extract the book name (e.g., 'Ru1') from the filename
            book_name = filename.split('_features.json')[0]
            
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Add the book name to the dictionary for easy identification
                data['translation'] = book_name
                all_features_list.append(data)
    
    if not all_features_list:
        print("ERROR: No feature files found. Make sure the script is in the same directory as your JSON files.")
        return pd.DataFrame()

    # Create the initial DataFrame from our list of dictionaries
    df = pd.DataFrame(all_features_list)
    
    # --- Select and Organize Columns for a Clean Summary Table ---
    # We will select the numerical features for direct comparison.
    summary_columns = [
        'translation',
        'total_word_count',
        'content_word_count',
        'unique_content_word_count',
        'avg_sentence_length',
        'chunked_ttr',
        'unigram_entropy',
        'bigram_entropy'
    ]
    
    # Filter out columns that might not exist (in case a feature wasn't calculated)
    # This makes the script more robust.
    existing_summary_columns = [col for col in summary_columns if col in df.columns]
    
    # Reorder the DataFrame with our selected columns and set the index
    summary_df = df[existing_summary_columns].set_index('translation')
    
    # Sort the DataFrame by translation name (Ru1, Ru2, etc.)
    summary_df = summary_df.sort_index()
    
    return summary_df

# --- Main Execution Block ---
if __name__ == '__main__':
    print("Loading features into a pandas DataFrame...")
    
    # Create the summary DataFrame
    features_df = load_features_to_dataframe()
    
    # Print the resulting table
    if not features_df.empty:
        print("\n--- Stylometric Feature Summary ---")
        print(features_df)
        
        # Save this summary table to a CSV file
        features_df.to_csv('stylometric_summary.csv')
        print("\nSummary table saved to 'stylometric_summary.csv'")