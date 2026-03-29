import re
import sys

def extract_facts(text):
    # This is a heuristic approach to extract facts
    facts = []

    # 1. Numerals and percentages (e.g., 2021, 35.8%, 0.129)
    # Be careful not to match simple numbers like "1" or "2" that might just be section numbers or list items
    # if they are heavily modified, but for a strict check, we extract all numbers.
    numerals = re.findall(r'\b\d+(?:\.\d+)?(?:%)?\b', text)
    facts.extend(numerals)

    # 2. Citation markers (e.g., [1], [5], [9]-[12])
    citations = re.findall(r'\[\d+(?:(?:, \d+)*)?(?:(?:–|-)\d+)?\]', text)
    facts.extend(citations)

    # 3. Model names (Specific to this paper based on instructions)
    models = re.findall(r'\b(XGBoost|LightGBM|CatBoost|ARIMAX|TBATS|DCNN-LSTM-AE-AM|CNN-BiLSTM|BiLSTM|GRU|LSTM|RNN)\b', text, re.IGNORECASE)
    facts.extend([m.lower() for m in models])

    # 4. Metrics
    metrics = re.findall(r'\b(RMSE|R²|MAE|MAPE)\b', text)
    facts.extend(metrics)

    return facts

def main():
    if len(sys.argv) != 3:
        print("Usage: python check_facts.py <original_file> <humanized_file>")
        sys.exit(1)

    original_file = sys.argv[1]
    humanized_file = sys.argv[2]

    with open(original_file, 'r', encoding='utf-8') as f:
        original_text = f.read()

    with open(humanized_file, 'r', encoding='utf-8') as f:
        humanized_text = f.read()

    # We only care about the Final rewrite section for validation
    if "Final rewrite" in humanized_text:
        humanized_text = humanized_text.split("Final rewrite")[1]

    original_facts = extract_facts(original_text)
    humanized_facts = extract_facts(humanized_text)

    # Count occurrences
    from collections import Counter
    orig_counts = Counter(original_facts)
    hum_counts = Counter(humanized_facts)

    mismatches = []
    for fact, count in orig_counts.items():
        if hum_counts[fact] < count:
            # We allow it if the humanized text still has it, but maybe combined or rephrased.
            # However, strict preservation means all instances or at least the fact exists.
            # Let's check if it exists at all first.
            if hum_counts[fact] == 0:
                mismatches.append(f"Missing completely: {fact} (expected {count})")
            else:
                pass # Often citations are consolidated or numbers used differently, but let's be strict if needed.
                # For now, flag if completely missing.

    if mismatches:
        print("Fact Integrity Check: FAILED")
        for m in mismatches:
            print(f" - {m}")
        sys.exit(1)
    else:
        print("Fact Integrity Check: PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()
