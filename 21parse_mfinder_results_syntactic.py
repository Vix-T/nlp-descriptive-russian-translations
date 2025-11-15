import os
import json
import re
from collections import defaultdict, Counter
import pathlib # Used to handle subfolders

def parse_members_file(filepath):
    """
    Reads the mfinder members file and groups the node IDs by motif type.
    Returns a dictionary: { "motif_id": [ (n1,n2,n3), (n4,n5,n6), ... ] }
    """
    if not os.path.exists(filepath):
        print(f"ERROR: Members file not found at '{filepath}'")
        return None

    motif_data = defaultdict(list)
    current_motif_id = None
    data_started = False  # Flag to track when we reach the data

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                if line.startswith("subgraph id ="):
                    header_parts = line.split()
                    if len(header_parts) == 4:
                        current_motif_id = header_parts[3] # Get the '6', '8', etc.
                    continue 

                if "members:" in line:
                    data_started = True
                    continue 

                if data_started and current_motif_id:
                    parts = line.split()
                    if len(parts) == 3: # Data lines have 3 node IDs
                        try:
                            nodes = tuple(sorted((int(parts[0]), int(parts[1]), int(parts[2]))))
                            motif_data[current_motif_id].append(nodes)
                        except ValueError:
                            continue # Skip any non-integer 3-part lines
    
    except Exception as e:
        print(f"ERROR: Failed to parse members file: {e}")
        return None

    if not motif_data:
        print(f"WARNING: No motif data found in {filepath}")

    return motif_data

def load_mapping(filepath):
    """Loads the word-to-ID JSON mapping file."""
    if not os.path.exists(filepath):
        print(f"ERROR: Mapping file not found at '{filepath}'")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load JSON mapping: {e}")
        return None

def create_reverse_mapping(word_to_id_map):
    """
    Creates an ID-to-Word mapping from a Word-to-ID map.
    """
    id_to_word_map = {}
    for word, node_id in word_to_id_map.items():
        id_to_word_map[node_id] = word
    return id_to_word_map

# --- Main Execution Block ---
if __name__ == "__main__":
    book_prefixes = ["Ru1", "Ru2", "Ru3", "Ru4", "Ru5"]
    
    data_folder = pathlib.Path("syntactic-analysis")
    
    print("--- Starting Syntactic Analysis Report Generation ---")
    
    for prefix in book_prefixes:
        print(f"\n--- Processing {prefix} ---")
        
        members_file = data_folder / f"{prefix}_syntactic_output_MEMBERS.txt"
        mapping_file = data_folder / f"{prefix}_syntactic_mapping.json"
        output_file = data_folder / f"{prefix}_syntactic_analysis_report.txt"

        word_map = load_mapping(mapping_file)
        if not word_map:
            print(f"   Skipping {prefix} due to missing mapping file.")
            continue
        
        id_map = create_reverse_mapping(word_map)
        print(f"   Loaded mapping: {len(id_map)} words.")
        
        motif_id_data = parse_members_file(members_file)
        if not motif_id_data:
            print(f"   Skipping {prefix} due to missing members file or parse error.")
            continue
        
        print(f"   Found {len(motif_id_data)} motif types in {members_file.name}.")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for motif_id, id_tuples in sorted(motif_id_data.items(), key=lambda item: int(item[0])):
                    
                    total_occurrences = len(id_tuples)
                    
                    word_clusters = []
                    for id_tuple in id_tuples:
                        try:
                            w1 = id_map[id_tuple[0]]
                            w2 = id_map[id_tuple[1]]
                            w3 = id_map[id_tuple[2]]
                            word_clusters.append(tuple(sorted((w1, w2, w3))))
                        except KeyError as e:
                            print(f"   WARNING: Could not find word for ID {e} in {prefix}")
                    
                    unique_clusters = set(word_clusters)
                    unique_count = len(unique_clusters)
                    
                    cluster_frequencies = Counter(word_clusters)
                    top_20_clusters = cluster_frequencies.most_common(20)

                    # Write the new, consistent report format
                    f.write(f"========================================\n")
                    f.write(f"## Results for Motif {motif_id} ##\n")
                    f.write(f"Total Occurrences (Nreal): {total_occurrences}\n")
                    f.write(f"Unique Word Clusters: {unique_count}\n\n")
                    
                    f.write(f"Top 20 Most Frequent Word Clusters:\n")
                    f.write(f"-------------------------------------\n")
                    for (w1, w2, w3), count in top_20_clusters:
                        f.write(f"  Count: {count}\tWords: {w1}, {w2}, {w3}\n")
                    f.write(f"========================================\n\n")
            
            print(f"Successfully saved report to {output_file}")
            
        except Exception as e:
            print(f"ERROR: Failed to write output file: {e}")

    print("\n--- All syntactic reports generated. ---")