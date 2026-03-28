import sys
import re

def extract_numbers(text):
    return set(re.findall(r'\b\d+(?:\.\d+)?\b', text))

def extract_uppercase_words(text):
    # Matches words with at least one uppercase letter (heuristic for names/acronyms)
    # excluding words at the very beginning of sentences (simplification)
    words = re.findall(r'\b[A-Z][a-zA-Z]*\b', text)
    # Filter out common starting words or just rely on a set intersection
    return set(words)

def main():
    if len(sys.argv) != 3:
        print("Usage: python check_facts.py <original> <humanized>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        orig = f.read()
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        hum = f.read()

    orig_nums = extract_numbers(orig)
    hum_nums = extract_numbers(hum)

    missing_nums = orig_nums - hum_nums

    # We will just do a soft check for acronyms/uppercase words to avoid false positives on sentence starts
    orig_caps = extract_uppercase_words(orig)
    hum_caps = extract_uppercase_words(hum)

    # Just look for obvious multi-letter acronyms or highly specific names that were dropped
    orig_acronyms = set(re.findall(r'\b[A-Z]{2,}\b', orig))
    hum_acronyms = set(re.findall(r'\b[A-Z]{2,}\b', hum))

    missing_acronyms = orig_acronyms - hum_acronyms

    errors = []
    if missing_nums:
        errors.append(f"Missing numbers in humanized text: {missing_nums}")
    if missing_acronyms:
        errors.append(f"Missing acronyms in humanized text: {missing_acronyms}")

    if errors:
        for err in errors:
            print(err)
        sys.exit(1)

    print("Facts (numbers and acronyms) successfully preserved.")
    sys.exit(0)

if __name__ == '__main__':
    main()