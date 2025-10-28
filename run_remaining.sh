#!/bin/bash

# This script runs the full mfinder analysis for texts 2-5,
# one after another. It uses the CORRECT rename command for
# the "..._MEMBERS.txt" file.

echo "--- Starting FULL mfinder sequential analysis (Ru2-Ru5) ---"
echo "This will run all remaining texts in order."

( \
    echo "[$(date)] Starting analysis for Ru2..." && \
    ./mfinder_mac/mfinder Ru2_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru2_mfinder_stats -omem -z 0 -m 0 -u 0 && \
    echo "[$(date)] Renaming Ru2 member list..." && \
    if [ -f Ru2_mfinder_stats_MEMBERS.txt ]; then \
        mv Ru2_mfinder_stats_MEMBERS.txt Ru2_mfinder_members_OUT.txt; \
    fi && \
    echo "[$(date)] Finished Ru2." && \
    
    echo "[$(date)] Starting analysis for Ru3..." && \
    ./mfinder_mac/mfinder Ru3_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru3_mfinder_stats -omem -z 0 -m 0 -u 0 && \
    echo "[$(date)] Renaming Ru3 member list..." && \
    if [ -f Ru3_mfinder_stats_MEMBERS.txt ]; then \
        mv Ru3_mfinder_stats_MEMBERS.txt Ru3_mfinder_members_OUT.txt; \
    fi && \
    echo "[$(date)] Finished Ru3." && \
    
    echo "[$(date)] Starting analysis for Ru4..." && \
    ./mfinder_mac/mfinder Ru4_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru4_mfinder_stats -omem -z 0 -m 0 -u 0 && \
    echo "[$(date)] Renaming Ru4 member list..." && \
    if [ -f Ru4_mfinder_stats_MEMBERS.txt ]; then \
        mv Ru4_mfinder_stats_MEMBERS.txt Ru4_mfinder_members_OUT.txt; \
    fi && \
    echo "[$(date)] Finished Ru4." && \
    
    echo "[$(date)] Starting analysis for Ru5..." && \
    ./mfinder_mac/mfinder Ru5_mfinder_input.txt -s 3 -r 100 -nsr 100 -f Ru5_mfinder_stats -omem -z 0 -m 0 -u 0 && \
    echo "[$(date)] Renaming Ru5 member list..." && \
    if [ -f Ru5_mfinder_stats_MEMBERS.txt ]; then \
        mv Ru5_mfinder_stats_MEMBERS.txt Ru5_mfinder_members_OUT.txt; \
    fi && \
    echo "[$(date)] Finished Ru5." && \
    
    echo "[$(date)] --- ALL ANALYSES ARE COMPLETE. ---" \
)