import json
import os

def create_mfinder_input_files(directory: str = '.'):
    """
    Reads feature files, converts bigram data to mfinder's edge list format,
    REMOVING SELF-LOOPS, and saves the corresponding input and mapping files.
    """
    print("--- Preparing input files for mfinder (v2 - No Self-Edges) ---")
    
    json_files = [f for f in os.listdir(directory) if f.endswith('_features.json')]

    for filename in sorted(json_files):
        book_name = filename.split('_features.json')[0]
        file_path = os.path.join(directory, filename)

        print(f"\nProcessing {book_name}...")

        # 1. Load the bigram data
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        bigram_freqs = data.get('bigram_frequencies')
        if not bigram_freqs:
            print(f"❌ No bigram data found for {book_name}. Skipping.")
            continue

        # 2. Create vocabulary and word-to-ID mapping
        vocabulary = set()
        for bigram in bigram_freqs.keys():
            word1, word2 = bigram.split('_')
            vocabulary.add(word1)
            vocabulary.add(word2)
        
        sorted_vocab = sorted(list(vocabulary))
        word_to_id = {word: i + 1 for i, word in enumerate(sorted_vocab)}

        # 3. Write the mfinder input file, SKIPPING self-edges
        mfinder_output_path = f"{book_name}_mfinder_input.txt"
        self_edge_count = 0
        with open(mfinder_output_path, 'w', encoding='utf-8') as f:
            for bigram, weight in bigram_freqs.items():
                word1, word2 = bigram.split('_')
                
                # --- THIS IS THE FIX ---
                # If the words in the bigram are the same, skip this entry.
                if word1 == word2:
                    self_edge_count += 1
                    continue
                # --- END OF FIX ---
                
                id1 = word_to_id[word1]
                id2 = word_to_id[word2]
                f.write(f"{id1} {id2} {weight}\n")
        
        print(f"✅ Created mfinder input file: {mfinder_output_path}")
        if self_edge_count > 0:
            print(f"   (Removed {self_edge_count} self-edges)")

        # 4. Save the word-to-ID mapping
        mapping_output_path = f"{book_name}_word_id_mapping.json"
        with open(mapping_output_path, 'w', encoding='utf-8') as f:
            json.dump(word_to_id, f, ensure_ascii=False, indent=4)
            
        print(f"✅ Saved word-to-ID map: {mapping_output_path}")

if __name__ == '__main__':
    create_mfinder_input_files()
    print("\n--- All files regenerated and are ready for mfinder analysis. ---")