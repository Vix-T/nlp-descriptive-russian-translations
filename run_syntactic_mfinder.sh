#!/bin/bash

# --- mfinder Analysis Script (for Syntactic Networks) ---
# This script finds all '_syntactic_input.txt' files and runs mfinder,
# ensuring that the members files are created.

echo "Starting sequential mfinder analysis..."

# Loop through each of the new input files
for input_file in *_syntactic_input.txt
do
    if [ -f "$input_file" ]; then
        echo "------------------------------------------"
        echo "Processing $input_file..."
        
        # Get the base name (e.g., "Ru1")
        # This removes the "_syntactic_input.txt" part
        output_name=$(basename "$input_file" _syntactic_input.txt)
        
        # Run mfinder
        # -s 3 : Find motifs of size 3 (matches our parser)
        # -om  : THIS IS THE KEY! It tells mfinder to "Output Members"
        # -f   : Specifies the prefix for all output files
        ./mfinder_mac/mfinder "$input_file" -s 3 -r 100 -omem -f "${output_name}_syntactic_output"
        
        echo "Completed analysis for $output_name."
    fi
done

echo "------------------------------------------"
echo "All syntactic mfinder analyses complete."