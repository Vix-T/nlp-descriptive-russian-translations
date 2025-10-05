import pandas as pd
import json
import os

def create_and_save_adjacency_matrix(file_path: str):
    """
    Loads bigram frequency data from a JSON feature file, creates an
    adjacency matrix, and saves it to a CSV file.

    Args:
        file_path (str): The path to the input '_features.json' file.
    """
    book_name = os.path.basename(file_path).split('_features.json')[0]
    print(f"--- Processing {book_name} ---")

    # Load the JSON data
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Extract the bigram frequency data
    bigram_freqs = data.get('bigram_frequencies')
    if not bigram_freqs:
        print(f"❌ No bigram frequency data found in {file_path}.")
        return

    # Convert the dictionary into a list of [word1, word2, count]
    edge_list = []
    for bigram, count in bigram_freqs.items():
        word1, word2 = bigram.split('_')
        edge_list.append([word1, word2, count])

    if not edge_list:
        print(f"❌ Edge list is empty for {book_name}.")
        return

    # Create a DataFrame from the edge list
    edge_df = pd.DataFrame(edge_list, columns=['word1', 'word2', 'weight'])

    # Pivot the DataFrame to create the adjacency matrix
    # The 'weight' (frequency) becomes the value in the matrix cells.
    adjacency_matrix = edge_df.pivot_table(index='word1', columns='word2', values='weight', fill_value=0)

    # Save the matrix to a CSV file
    output_filename = f'adjacency_matrix_{book_name}.csv'
    adjacency_matrix.to_csv(output_filename, encoding='utf-8-sig')
    print(f"✅ Adjacency matrix saved to {output_filename}")


if __name__ == '__main__':
    print("--- Generating Bi-gram Adjacency Matrices ---")
    
    # Find all feature files in the current directory
    for filename in sorted(os.listdir('.')):
        if filename.endswith('_features.json'):
            create_and_save_adjacency_matrix(filename)
            
    print("\n--- All matrices created successfully! ---")