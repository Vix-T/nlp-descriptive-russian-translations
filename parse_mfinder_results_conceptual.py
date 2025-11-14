import os
import json
from collections import Counter, defaultdict

def load_word_map(filepath):
    """
    Loads the { "word": "id" } mapping from a JSON file and "flips" it
    to create an { id: word } map.
    """
    if not os.path.exists(filepath):
        print(f"❌ ERROR: Word map file not found at '{filepath}'")
        return None
    
    id_to_word = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            word_to_id_map = json.load(f)
            # "Flip" the map to be { id: word }
            id_to_word = {int(value): key for key, value in word_to_id_map.items()}
        return id_to_word
    except Exception as e:
        print(f"❌ ERROR: Failed to read or process word map: {e}")
        return None

def parse_members_file(filepath):
    """
    Reads the mfinder members file and groups the node IDs by motif type.
    The motif ID is assumed to be in the header "subgraph id = X".
    Returns a dictionary: { "motif_id": [ (n1,n2,n3), (n4,n5,n6), ... ] }
    """
    if not os.path.exists(filepath):
        print(f"❌ ERROR: Members file not found at '{filepath}'")
        return None

    motif_data = defaultdict(list)
    current_motif_id = None
    data_started = False  # Flag to track when we reach the data

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # 1. Look for the motif ID in the header first
                if line.startswith("subgraph id ="):
                    header_parts = line.split()
                    if len(header_parts) == 4:
                        current_motif_id = header_parts[3] # Get the '6'
                    continue # Go to the next line

                # 2. Look for the start of the data list
                if "members:" in line:
                    data_started = True
                    continue # Go to the next line

                # 3. If we are in the data section and have a motif ID, process lines
                if data_started and current_motif_id:
                    
                    # This is our new check for data lines
                    parts = line.split()
                    if len(parts) == 3:
                        try:
                            # Now we process the 3 parts as nodes
                            nodes = tuple(sorted((int(parts[0]), int(parts[1]), int(parts[2]))))
                            motif_data[current_motif_id].append(nodes)
                        except ValueError:
                            # This will skip any 3-part lines that aren't numbers
                            # (e.g., if there was a "--- --- ---" line)
                            continue

    except Exception as e:
        print(f"❌ ERROR: Failed to parse members file: {e}")
        return None

    if not current_motif_id:
        # This will help you know if a file was processed but no ID was found
        print(f"⚠️ WARNING: Could not find 'subgraph id' in header of {filepath}")

    return motif_data

# --- Main Script ---
if __name__ == "__main__":
    
    # List of all motif IDs we expect from mfinder
    ALL_MOTIF_IDS = ['6', '12', '14', '36', '38', '46', '74', '78', '98', '102', '108', '110', '238']
    
    # Loop through all 5 books
    for i in range(1, 6):
        book_id = f"Ru{i}"
        print(f"\n--- Processing {book_id} ---")

        word_map_file = f"{book_id}_word_id_mapping.json"
        members_file = f"{book_id}_mfinder_members_OUT.txt"
        output_file = f"{book_id}_motif_analysis_report.txt"

        # Load the two required files
        id_to_word_map = load_word_map(word_map_file)
        motif_data = parse_members_file(members_file)

        if not id_to_word_map or not motif_data:
            print(f"--- Skipping {book_id} due to missing files. ---")
            continue

        # Write the final report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Motif Analysis Report for: {book_id}\n")
            f.write("="*40 + "\n\n")

            for motif_id in ALL_MOTIF_IDS:
                f.write(f"## Results for Motif {motif_id} ##\n")
                
                # Get the list of numeric instances for this motif
                numeric_instances = motif_data.get(motif_id)
                
                if not numeric_instances:
                    f.write("Total Occurrences (Nreal): 0\n\n")
                    f.write("\n" + "="*40 + "\n\n")
                    continue
                
                # Get the total count
                total_occurrences = len(numeric_instances)
                
                # Count the frequency of each unique numeric triplet
                instance_counts = Counter(numeric_instances)
                unique_clusters = len(instance_counts)

                f.write(f"Total Occurrences (Nreal): {total_occurrences}\n")
                f.write(f"Unique Word Clusters: {unique_clusters}\n\n")

                f.write("Top 20 Most Frequent Word Clusters:\n")
                f.write("-------------------------------------\n")

                # Get the top 20 most common numeric triplets
                top_20 = instance_counts.most_common(20)
                
                # Translate them to words for the report
                for num_instance, count in top_20:
                    words = tuple(sorted(
                        (id_to_word_map.get(node_id, '???') for node_id in num_instance)
                    ))
                    f.write(f"  Count: {count}\tWords: {', '.join(words)}\n")
                
                f.write("\n" + "="*40 + "\n\n")

        print(f"✅ Analysis complete for {book_id}. Results saved to '{output_file}'")

    print("\n--- All 5 texts have been processed. ---")