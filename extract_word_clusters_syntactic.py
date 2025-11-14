import os
import json
from collections import defaultdict

# --- This is the parser function we fixed before ---
def parse_members_file(filepath):
    """
    Reads the mfinder members file and groups the node IDs by motif type.
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

                # 1. Look for the motif ID in the header
                if line.startswith("subgraph id ="):
                    header_parts = line.split()
                    if len(header_parts) == 4:
                        current_motif_id = header_parts[3] # Get the '6', '8', etc.
                    continue 

                # 2. Look for the start of the data list
                if "members:" in line:
                    data_started = True
                    continue 

                # 3. If we are in the data section, process lines
                if data_started and current_motif_id:
                    parts = line.split()
                    if len(parts) == 3: # Data lines have 3 node IDs
                        try:
                            nodes = tuple(sorted((int(parts[0]), int(parts[1]), int(parts[2]))))
                            motif_data[current_motif_id].append(nodes)
                        except ValueError:
                            continue # Skip any non-integer 3-part lines
    
    except Exception as e:
        print(f"❌ ERROR: Failed to parse members file: {e}")
        return None

    if not motif_data:
        print(f"⚠️ WARNING: No motif data found in {filepath}")

    return motif_data

# --- New functions to load mapping and translate IDs ---

def load_mapping(filepath):
    """Loads the word-to-ID JSON mapping file."""
    if not os.path.exists(filepath):
        print(f"❌ ERROR: Mapping file not found at '{filepath}'")
        return None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ ERROR: Failed to load JSON mapping: {e}")
        return None

def create_reverse_mapping(word_to_id_map):
    """
    Creates an ID-to-Word mapping from a Word-to-ID map.
    Our map is {word: id}, so we just invert it.
    """
    id_to_word_map = {}
    for word, node_id in word_to_id_map.items():
        id_to_word_map[node_id] = word
    return id_to_word_map

# --- Main Execution ---

if __name__ == "__main__":
    book_prefixes = ["Ru1", "Ru2", "Ru3", "Ru4", "Ru5"]
    
    print("--- Starting Syntactic Word Cluster Extraction ---")
    
    for prefix in book_prefixes:
        print(f"\n--- Processing {prefix} ---")
        
        # --- THIS IS THE CORRECTED LINE ---
        members_file = f"{prefix}_syntactic_output_MEMBERS.txt"
        # --- END OF FIX ---
        
        mapping_file = f"{prefix}_syntactic_mapping.json"
        output_file = f"{prefix}_syntactic_clusters.txt"

        # 2. Load Word-to-ID map and create reverse (ID-to-Word) map
        word_map = load_mapping(mapping_file)
        if not word_map:
            continue
        
        id_map = create_reverse_mapping(word_map)
        print(f"Loaded mapping: {len(id_map)} words.")
        
        # 3. Parse the .members file to get ID clusters
        motif_id_data = parse_members_file(members_file)
        if not motif_id_data:
            continue
        
        print(f"Found {len(motif_id_data)} motif types in {members_file}.")
        
        # 4. Translate ID clusters to Word clusters and save
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for motif_id, id_tuples in motif_id_data.items():
                    f.write(f"\n=================================\n")
                    f.write(f"Motif ID: {motif_id} (Found {len(id_tuples)} times)\n")
                    f.write(f"=================================\n")
                    
                    word_clusters = []
                    for id_tuple in id_tuples:
                        try:
                            # Translate tuple of 3 IDs to tuple of 3 words
                            w1 = id_map[id_tuple[0]]
                            w2 = id_map[id_tuple[1]]
                            w3 = id_map[id_tuple[2]]
                            word_clusters.append(tuple(sorted((w1, w2, w3))))
                        except KeyError as e:
                            print(f"⚠️ WARNING: Could not find word for ID {e} in {prefix}")
                    
                    # Write all word clusters for this motif
                    for cluster in word_clusters:
                        # {:<20} adds padding to align the columns
                        f.write(f"{cluster[0]:<20} {cluster[1]:<20} {cluster[2]:<20}\n")
            
            print(f"✅ Successfully saved word clusters to {output_file}")
            
        except Exception as e:
            print(f"❌ ERROR: Failed to write output file: {e}")

    print("\n--- All word clusters extracted. ---")