#!/bin/bash

echo "--- STARTING FULL CONCEPTUAL NETWORK ANALYSIS ---"

# Step 1: Activate Python Environment
echo "Activating Python virtual environment..."
source .venv/bin/activate

# Step 2: Run Phase 1 & 2 (Data Prep)
echo "Running 01 (Lemmatization)..."
python 01dataprep_clean_lemmatize.py
echo "Running 02 (Stopword Removal)..."
python 02dataprep_removestopwords.py
echo "Running 03 (Feature Extraction)..."
python 03feature_extraction.py

# Step 3: Run Phase 4 Prep script
# This creates the input files in the 'conceptual-analysis/' folder
echo "Running Python prep script (17mfinder-prep.py)..."
python 17mfinder-prep.py

# Step 4: Change to the output directory
echo "Changing to 'conceptual-analysis' directory..."
cd conceptual-analysis/

# Step 5: Loop through and run mfinder on each input file
echo "Running mfinder on all '_mfinder_input.txt' files..."
for input_file in *_mfinder_input.txt
do
    if [ -f "$input_file" ]; then
        echo "------------------------------------------"
        echo "Processing $input_file..."
        
        # Get the base name (e.g., "Ru1")
        output_name=$(basename "$input_file" _mfinder_input.txt)
        
        # Run mfinder
        # We use ../mfinder_mac/ because we are one directory deep
        ../mfinder_mac/mfinder "$input_file" -s 3 -r 100 -omem -f "${output_name}_conceptual_output"
        
        echo "Completed analysis for $output_name."
    fi
done

# Step 6: Return to the main project directory
cd ..
echo "------------------------------------------"
echo "All conceptual mfinder analyses complete."