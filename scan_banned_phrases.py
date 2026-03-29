import re
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python scan_banned_phrases.py <original_file> <humanized_file>")
        sys.exit(1)

    humanized_file = sys.argv[2]

    with open(humanized_file, 'r', encoding='utf-8') as f:
        humanized_text = f.read()

    if "Final rewrite" in humanized_text:
        humanized_text = humanized_text.split("Final rewrite")[1]

    # Read taboo phrases from references/taboo-phrases.md
    with open('references/taboo-phrases.md', 'r', encoding='utf-8') as f:
        taboo_md = f.read()

    # Extract Category A phrases
    cat_a_match = re.search(r'## Category A: Always remove(.*?)## Category B', taboo_md, re.DOTALL)
    cat_a_phrases = []
    if cat_a_match:
        lines = cat_a_match.group(1).split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('- '):
                phrase = line[2:].strip().strip('"')
                if phrase:
                    cat_a_phrases.append(phrase)

    found_phrases = []
    for phrase in cat_a_phrases:
        # Simple case-insensitive match
        if re.search(r'\b' + re.escape(phrase) + r'\b', humanized_text, re.IGNORECASE):
            found_phrases.append(phrase)

    if found_phrases:
        print("Taboo Phrase Scan: FAILED")
        for p in found_phrases:
            print(f" - Found banned phrase: '{p}'")
        sys.exit(1)
    else:
        print("Taboo Phrase Scan: PASSED (Zero instances of Category A taboo phrases)")
        sys.exit(0)

if __name__ == "__main__":
    main()
