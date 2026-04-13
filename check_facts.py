import sys
import re

def extract_facts(text):
    facts = []
    # Extract numbers
    facts.extend(re.findall(r'\b\d+(?:\.\d+)?\b', text))
    # Extract LaTeX commands
    facts.extend(re.findall(r'\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\{[^}]*\})*', text))
    # Extract model names
    facts.extend(re.findall(r'\b(?:XGBoost|LightGBM|ARIMAX|CatBoost)\b', text))
    # Extract metrics
    facts.extend(re.findall(r'\b(?:RMSE|R²|f1_weighted)\b', text))
    return facts

def main():
    if len(sys.argv) != 3:
        print("Usage: python check_facts.py <original_file> <humanized_file>")
        sys.exit(1)

    original_file = sys.argv[1]
    humanized_file = sys.argv[2]

    with open(original_file, 'r') as f:
        original_text = f.read()

    with open(humanized_file, 'r') as f:
        humanized_text = f.read()

    original_facts = extract_facts(original_text)

    # We want to check that all extracted facts from the original exist in the humanized version.
    missing_facts = []
    for fact in original_facts:
        if fact not in humanized_text:
            missing_facts.append(fact)

    if missing_facts:
        print("FAIL: The following facts were missing or modified in the humanized text:")
        for fact in set(missing_facts):
            print(f"  - {fact}")
        sys.exit(1)
    else:
        print("PASS: Fact Integrity Check.")
        sys.exit(0)

if __name__ == "__main__":
    main()
