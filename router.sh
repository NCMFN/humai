#!/usr/bin/env bash

# This script acts as the traffic router for the Humanizer tool.
# It requires `jq` and `curl` to interact with an LLM API, or it can be adapted
# to use the `claude` CLI if installed.

ORIGINAL_FILE=$1
HUMANIZED_FILE=$2

if [ -z "$ORIGINAL_FILE" ] || [ -z "$HUMANIZED_FILE" ]; then
    echo "Usage: ./router.sh <original_file> <output_file>"
    exit 1
fi

echo "--- Humanizer Traffic Router ---"

# Check if validation scripts exist
for script in check_facts.py scan_banned_phrases.py measure_readability.py flag_changes.py; do
    if [ ! -f "validation/$script" ]; then
        echo "Error: Validation script validation/$script not found."
        exit 1
    fi
done

# We assume the user has provided the text in ORIGINAL_FILE, and we must humanize it.
# Since this script runs in an environment where we might not have a direct LLM API key,
# we will prompt the user to use the LLM to write the HUMANIZED_FILE, and then we run validations.

if [ ! -f "$HUMANIZED_FILE" ]; then
    echo "The file $HUMANIZED_FILE does not exist. Please humanize $ORIGINAL_FILE using an LLM and save the result to $HUMANIZED_FILE."
    echo "Then run this script again to validate."
    exit 0
fi

echo "Validating $HUMANIZED_FILE against $ORIGINAL_FILE..."

# Run Pass 1 (Validations)
echo "[1/4] Checking Facts..."
python3 validation/check_facts.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
if [ $? -ne 0 ]; then
    echo "Fact check failed."
    exit 1
fi

echo "[2/4] Scanning for Banned Phrases..."
python3 validation/scan_banned_phrases.py "$HUMANIZED_FILE" references/taboo-phrases.md
if [ $? -ne 0 ]; then
    echo "Banned phrases found."
    exit 1
fi

echo "[3/4] Measuring Readability..."
python3 validation/measure_readability.py "$HUMANIZED_FILE"
if [ $? -ne 0 ]; then
    echo "Readability check failed."
    exit 1
fi

echo "[4/4] Flagging Changes..."
python3 validation/flag_changes.py "$ORIGINAL_FILE" "$HUMANIZED_FILE"
if [ $? -ne 0 ]; then
    echo "Change check failed."
    exit 1
fi

echo "SUCCESS: The text in $HUMANIZED_FILE has been successfully humanized and passed all validations."
exit 0
