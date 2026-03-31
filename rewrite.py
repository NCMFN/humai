import sys
import re

def extract_facts(text):
    facts = []
    # Extract numbers
    facts.extend(re.findall(r'\b\d+(?:\.\d+)?(?:%|GHz|ms|Tbps|Gbps|μs)?\b', text))
    # Proper Nouns (capitalized sequences)
    facts.extend(re.findall(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b', text))
    return set(facts)

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        text = f.read()
    facts = extract_facts(text)
    print(f"Extracted {len(facts)} unique fact tokens from input.txt")
