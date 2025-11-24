#!/bin/bash

echo "--- STARTING FULL NETWORK ANALYSIS ---"

# Step 1: Activate Python Environment
echo "Activating Python virtual environment..."
source .venv/bin/activate

# Step 2: Run Phase 1 & 2 (Data Prep)
echo "Running 01 (Lemmatization)..."
python 01dataprep_clean_lemmatize
echo "Running 02 (Stopword Removal)..."
python 02dataprep_removestopwords
echo "Running 03 (Feature Extraction)..."
python 03feature_extraction

# Step 3: Run Phase 4 Prep script
echo "Running Python prep script (17create_mfinder_network)..."
python 17create_mfinder_network

# Step 4: Change to the output directory
echo "Changing to 'mfinder-analysis' directory..."
cd mfinder-analysis/

# Step 5: Loop through and run mfinder on each input file
echo "Running mfinder on all '_mfinder_input.txt' files..."
for input_file in *_mfinder_input.txt
do
    if [ -f "$input_file" ]; then
        echo "------------------------------------------"
        echo "Processing $input_file..."
        
        output_name=$(basename "$input_file" _mfinder_input.txt)
        
        ../mfinder_mac/mfinder "$input_file" -s 3 -r 100 -omem -f "${output_name}_output"
        
        echo "Completed analysis for $output_name."
    fi
done

# Step 6: Return to the main project directory
cd ..
echo "------------------------------------------"
echo "All mfinder analyses complete."