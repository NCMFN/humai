import sys
import re

def load_taboo_phrases(taboo_file):
    phrases = []
    try:
        with open(taboo_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('- '):
                    # Extract the actual phrase, ignoring anything in parentheses or quotes
                    # e.g., "- "In order to" (use "To")" -> "in order to"
                    # Handle cases with and without quotes
                    match = re.search(r'- "?([^"\(]+)"?', line)
                    if match:
                        phrase = match.group(1).lower().strip('., ')
                        if phrase and phrase not in ['features']:
                            phrases.append(phrase)
                    else:
                        phrase = line[2:].lower().strip('., ')
                        if phrase and phrase not in ['features']:
                            phrases.append(phrase)
    except Exception as e:
        print(f"Error reading taboo phrases file: {e}")
    return phrases

def scan_banned_phrases(humanized_file, taboo_file):
    try:
        taboo_phrases = load_taboo_phrases(taboo_file)
        if not taboo_phrases:
            print("No taboo phrases found to scan against.")
            return False

        with open(humanized_file, 'r') as f:
            content = f.read()

        found_phrases = []
        for phrase in taboo_phrases:
            # Try exact word match first (case-insensitive)
            # We specifically look for word boundaries, so "DelveInsight" doesn't trigger "delve"
            # And ignore quotes inside citations like "... myriad ..."
            # We do this by searching only outside quotes, or just reporting everything and manually overriding.
            # Actually, the rubric says "Quotes are the literal words of a source and must remain perfectly intact... even if it violates the taboo-phrases.md list"
            # Let's remove content inside quotes before scanning.
            content_without_quotes = re.sub(r'["“][^"”]*["”]', '', content)

            if re.search(r'\b' + re.escape(phrase) + r'\b', content_without_quotes, re.IGNORECASE):
                found_phrases.append(phrase)

        if found_phrases:
            print("ERROR: Found banned phrases in humanized text:")
            for p in found_phrases:
                print(f"  - {p}")
            return False

        print("SUCCESS: No banned phrases found.")
        return True

    except Exception as e:
        print(f"Error scanning for banned phrases: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scan_banned_phrases.py <humanized_file> <taboo_phrases_file>")
        sys.exit(1)
    success = scan_banned_phrases(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
