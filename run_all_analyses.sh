#!/bin/bash

# This script runs the full mfinder analysis for all 5 texts,
# one after another. It uses the '-omem' flag to get the
# full list of motif members (the word IDs).

echo "--- Starting FULL mfinder sequential analysis (with -omem) ---"
echo "This will run all 5 texts in order. This will take a very long time."
echo "The computer must not be allowed to sleep."

( \
    echo "[$(date)] Starting analysis for Ru1..." && \
    ./mfinder_mac/mfinder Ru1_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru1_mfinder_stats_OUT.txt -omem && \
    echo "[$(date)] Renaming Ru1 member list..." && \
    mv Ru1_mfinder_input.txt__MEM.txt Ru1_mfinder_members_OUT.txt && \
    echo "[$(date)] Finished Ru1." && \
    
    echo "[$(date)] Starting analysis for Ru2..." && \
    ./mfinder_mac/mfinder Ru2_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru2_mfinder_stats_OUT.txt -omem && \
    echo "[$(date)] Renaming Ru2 member list..." && \
    mv Ru2_mfinder_input.txt__MEM.txt Ru2_mfinder_members_OUT.txt && \
    echo "[$(date)] Finished Ru2." && \
    
    echo "[$(date)] Starting analysis for Ru3..." && \
    ./mfinder_mac/mfinder Ru3_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru3_mfinder_stats_OUT.txt -omem && \
    echo "[$(date)] Renaming Ru3 member list..." && \
    mv Ru3_mfinder_input.txt__MEM.txt Ru3_mfinder_members_OUT.txt && \
    echo "[$(date)] Finished Ru3." && \
    
    echo "[$(date)] Starting analysis for Ru4..." && \
    ./mfinder_mac/mfinder Ru4_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru4_mfinder_stats_OUT.txt -omem && \
    echo "[$(date)] Renaming Ru4 member list..." && \
    mv Ru4_mfinder_input.txt__MEM.txt Ru4_mfinder_members_OUT.txt && \
    echo "[$(date)] Finished Ru4." && \
    
    echo "[$(date)] Starting analysis for Ru5..." && \
    ./mfinder_mac/mfinder Ru5_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru5_mfinder_stats_OUT.txt -omem && \
    echo "[$(date)] Renaming Ru5 member list..." && \
    mv Ru5_mfinder_input.txt__MEM.txt Ru5_mfinder_members_OUT.txt && \
    echo "[$(date)] Finished Ru5." && \
    
    echo "[$(date)] --- ALL ANALYSES ARE COMPLETE. ---" \
)