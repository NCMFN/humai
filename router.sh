#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./router.sh <original_file> <humanized_file>"
    exit 1
fi

ORIGINAL=$1
HUMANIZED=$2
TABOO_FILE="references/taboo-phrases.md"

echo "Running Validation Scripts on $HUMANIZED..."
echo "=========================================="

echo "[1/4] Checking Fact Preservation..."
python check_facts.py "$ORIGINAL" "$HUMANIZED"
if [ $? -ne 0 ]; then
    echo "=> Validation Failed at check_facts.py"
    exit 1
fi
echo ""

echo "[2/4] Scanning Banned Phrases..."
python scan_banned_phrases.py "$TABOO_FILE" "$HUMANIZED"
if [ $? -ne 0 ]; then
    echo "=> Validation Failed at scan_banned_phrases.py"
    exit 1
fi
echo ""

echo "[3/4] Measuring Readability..."
python measure_readability.py "$HUMANIZED"
if [ $? -ne 0 ]; then
    echo "=> Validation Failed at measure_readability.py"
    exit 1
fi
echo ""

echo "[4/4] Flagging Significant Changes..."
python flag_changes.py "$ORIGINAL" "$HUMANIZED"
if [ $? -ne 0 ]; then
    echo "=> Validation Failed at flag_changes.py"
    exit 1
fi
echo ""

echo "All Validation Checks Passed Successfully!"
exit 0