import sys

CATEGORY_A_PHRASES = [
    "delve",
    "underscore the importance of",
    "it is worth noting that",
    "this paper leverages",
    "robust framework",
    "shed light on",
    "multifaceted",
    "it is imperative that"
]

def main():
    if len(sys.argv) != 3:
        print("Usage: python scan_banned_phrases.py <original_file> <humanized_file>")
        sys.exit(1)

    humanized_file = sys.argv[2]

    with open(humanized_file, 'r') as f:
        humanized_text = f.read().lower()

    found_phrases = []
    for phrase in CATEGORY_A_PHRASES:
        if phrase in humanized_text:
            found_phrases.append(phrase)

    if found_phrases:
        print("FAIL: Found Category A taboo phrases in the humanized text:")
        for phrase in found_phrases:
            print(f"  - {phrase}")
        sys.exit(1)
    else:
        print("PASS: Taboo Phrase Scan.")
        sys.exit(0)

if __name__ == "__main__":
    main()
