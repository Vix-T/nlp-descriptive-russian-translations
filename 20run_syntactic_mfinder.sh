#!/bin/bash

echo "--- STARTING FULL SYNTACTIC NETWORK ANALYSIS ---"

# Step 1: Activate Python Environment
echo "Activating Python virtual environment..."
source .venv/bin/activate

# Step 2: Run the Python prep script
echo "Running Python prep script (18create_syntactic_network)..."
# --- THIS LINE IS UPDATED ---
python 18create_syntactic_network

# Step 3: Change to the output directory
echo "Changing to 'syntactic-analysis' directory..."
cd syntactic-analysis/

# Step 4: Loop through and run mfinder on each input file
echo "Running mfinder on all '_syntactic_input.txt' files..."
for input_file in *_syntactic_input.txt
do
    if [ -f "$input_file" ]; then
        echo "------------------------------------------"
        echo "Processing $input_file..."
        
        output_name=$(basename "$input_file" _syntactic_input.txt)
        
        ../mfinder_mac/mfinder "$input_file" -s 3 -r 100 -omem -f "${output_name}_syntactic_output"
        
        echo "Completed analysis for $output_name."
    fi
done

# Step 5: Return to the main project directory
cd ..
echo "------------------------------------------"
echo "All syntactic mfinder analyses complete."