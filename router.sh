#!/bin/bash

# router.sh - Executes the four validation scripts
# Usage: ./router.sh <original_file> <humanized_file>

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <original_file> <humanized_file>"
    exit 1
fi

ORIGINAL_FILE="$1"
HUMANIZED_FILE="$2"

echo "Running Validation Pipeline..."
echo "------------------------------"

echo "1. Fact Integrity Check"
python3 check_facts.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
FACT_EXIT_CODE=$?
echo ""

echo "2. Taboo Phrase Scanner"
python3 scan_banned_phrases.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
SCAN_EXIT_CODE=$?
echo ""

echo "3. Readability and Rhythm Audit"
python3 measure_readability.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
READ_EXIT_CODE=$?
echo ""

echo "4. Drift Detection (Change Ratio)"
python3 flag_changes.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
DRIFT_EXIT_CODE=$?
echo ""

echo "------------------------------"
if [ $FACT_EXIT_CODE -eq 0 ] && [ $SCAN_EXIT_CODE -eq 0 ] && [ $READ_EXIT_CODE -eq 0 ] && [ $DRIFT_EXIT_CODE -eq 0 ]; then
    echo "All checks PASSED."
    exit 0
else
    echo "One or more checks FAILED."
    exit 1
fi
