import sys
import re

def main():
    if len(sys.argv) != 3:
        print("Usage: python scan_banned_phrases.py <taboo_file> <humanized_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        taboo_content = f.read()

    # Extract list items from the markdown taboo file
    banned_phrases = []
    for line in taboo_content.split('\n'):
        if line.startswith('- '):
            phrase = line.replace('- ', '').strip().lower()
            banned_phrases.append(phrase)

    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        humanized_text = f.read().lower()

    found_phrases = []
    for phrase in banned_phrases:
        # Avoid partial word matches
        pattern = r'\b' + re.escape(phrase) + r'\b'
        if re.search(pattern, humanized_text):
            found_phrases.append(phrase)

    if found_phrases:
        print(f"Failed! Found banned phrases: {found_phrases}")
        sys.exit(1)

    print("Pass: No banned phrases detected.")
    sys.exit(0)

if __name__ == '__main__':
    main()