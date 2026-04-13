#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./router.sh <original_file> <humanized_file>"
    exit 1
fi

ORIGINAL_FILE="$1"
HUMANIZED_FILE="$2"

echo "Running Validation Pipeline on $HUMANIZED_FILE..."

# Check Facts
python3 check_facts.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
if [ $? -ne 0 ]; then
    echo "Pipeline aborted due to Fact Integrity Check failure."
    exit 1
fi

# Scan Taboo Phrases
python3 scan_banned_phrases.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
if [ $? -ne 0 ]; then
    echo "Pipeline aborted due to Taboo Phrase Scan failure."
    exit 1
fi

# Measure Readability
python3 measure_readability.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
if [ $? -ne 0 ]; then
    echo "Pipeline aborted due to Readability Metrics failure."
    exit 1
fi

# Flag Changes
python3 flag_changes.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
if [ $? -ne 0 ]; then
    echo "Pipeline aborted due to Change Threshold Check failure."
    exit 1
fi

echo "All checks passed! The text has been successfully humanized and validated."
exit 0
