import os
import json
from collections import Counter, defaultdict
import pathlib # Import pathlib to handle sub-directories

def load_word_map(filepath):
    """
    Loads the { "word": "id" } mapping from a JSON file and "flips" it
    to create an { id: word } map.
    """
    if not os.path.exists(filepath):
        print(f"ERROR: Word map file not found at '{filepath}'")
        return None
    
    id_to_word = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            word_to_id_map = json.load(f)
            # "Flip" the map to be { id: word }
            id_to_word = {int(value): key for key, value in word_to_id_map.items()}
        return id_to_word
    except Exception as e:
        print(f"ERROR: Failed to read or process word map: {e}")
        return None

def parse_members_file(filepath):
    """
    Reads the mfinder members file and groups the node IDs by motif type.
    """
    if not os.path.exists(filepath):
        print(f"ERROR: Members file not found at '{filepath}'")
        return None

    motif_data = defaultdict(list)
    current_motif_id = None
    data_started = False 

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if line.startswith("subgraph id ="):
                    header_parts = line.split()
                    if len(header_parts) == 4:
                        current_motif_id = header_parts[3]
                    continue 

                if "members:" in line:
                    data_started = True
                    continue 

                if data_started and current_motif_id:
                    parts = line.split()
                    if len(parts) == 3:
                        try:
                            nodes = tuple(sorted((int(parts[0]), int(parts[1]), int(parts[2]))))
                            motif_data[current_motif_id].append(nodes)
                        except ValueError:
                            continue
    except Exception as e:
        print(f"ERROR: Failed to parse members file: {e}")
        return None

    if not motif_data:
        print(f"WARNING: No motif data found in {filepath}")
        
    return motif_data

# --- Main Script ---
if __name__ == "__main__":
    
    ALL_MOTIF_IDS = ['6', '12', '14', '36', '38', '46', '74', '78', '98', '102', '108', '110', '238']
    
    # --- FIXED: Define the subfolder ---
    data_folder = pathlib.Path("conceptual-analysis")

    print("--- Starting Conceptual Analysis Report Generation ---")
    
    for i in range(1, 6):
        book_id = f"Ru{i}"
        print(f"\n--- Processing {book_id} ---")

        # --- FIXED: Update all file paths to use the subfolder ---
        word_map_file = data_folder / f"{book_id}_word_id_mapping.json"
        members_file = data_folder / f"{book_id}_conceptual_output_MEMBERS.txt"
        output_file = data_folder / f"{book_id}_conceptual_analysis_report.txt"
        # --- END OF FIXES ---

        id_to_word_map = load_word_map(word_map_file)
        motif_data = parse_members_file(members_file)

        if not id_to_word_map or not motif_data:
            print(f"--- Skipping {book_id} due to missing files. ---")
            continue

        print(f"   Loaded mapping: {len(id_to_word_map)} words.")
        print(f"   Found {len(motif_data)} motif types in {members_file.name}.")

        # Write the final report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Motif Analysis Report for: {book_id}\n")
            f.write("="*40 + "\n\n")

            for motif_id in ALL_MOTIF_IDS:
                f.write(f"## Results for Motif {motif_id} ##\n")
                
                numeric_instances = motif_data.get(motif_id)
                
                if not numeric_instances:
                    f.write("Total Occurrences (Nreal): 0\n\n")
                    f.write("\n" + "="*40 + "\n\n")
                    continue
                
                total_occurrences = len(numeric_instances)
                instance_counts = Counter(numeric_instances)
                unique_clusters = len(instance_counts)

                f.write(f"Total Occurrences (Nreal): {total_occurrences}\n")
                f.write(f"Unique Word Clusters: {unique_clusters}\n\n")

                f.write("Top 20 Most Frequent Word Clusters:\n")
                f.write("-------------------------------------\n")

                top_20 = instance_counts.most_common(20)
                
                for num_instance, count in top_20:
                    words = tuple(sorted(
                        (id_to_word_map.get(node_id, '???') for node_id in num_instance)
                    ))
                    f.write(f"  Count: {count}\tWords: {', '.join(words)}\n")
                
                f.write("\n" + "="*40 + "\n\n")

        print(f"Analysis complete for {book_id}. Results saved to '{output_file}'")

    print("\n--- All 5 texts have been processed. ---")