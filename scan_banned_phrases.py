import sys

# Categorized inventory of AI-isms to eliminate
BANNED = [
    r'\bdelve\b', r'\bunderscore the importance of\b', r'\bshed light on\b', r'\bmultifaceted\b',
    r'\bIt is worth noting that\b', r'\bThis paper leverages\b', r'\bIt is imperative that\b',
    r'\bstands as\b', r'\bserves as\b', r'\bis a testament to\b', r'\bpivotal moment\b',
    r'\bevolving landscape\b', r'\bdeeply rooted\b', r'\bshowcase\b', r'\bhighlighting\b',
    r'\bunderscoring\b', r'\bemphasizing\b', r'\breflecting\b', r'\bsymbolizing\b', r'\bcontributing to\b',
    r'\bcultivating\b', r'\bfostering\b', r'\bencompassing\b', r'\bThe remainder of this paper is organized as follows\b'
]

import re

if __name__ == '__main__':
    try:
        with open(sys.argv[2], 'r') as f:
            text = f.read().lower()

        issues = []
        for phrase in BANNED:
            if re.search(phrase, text, re.IGNORECASE):
                issues.append(phrase.replace(r'\b', ''))

        if issues:
            print(f"Taboo Phrase Check: FAILED. Found: {', '.join(issues)}")
        else:
            print("Taboo Phrase Check: PASSED.")
    except Exception as e:
        print(f"Error checking phrases: {e}")
