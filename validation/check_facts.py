import sys
import re

def extract_numbers(text):
    return set(re.findall(r'\b\d+(?:\.\d+)?\b', text))

def check_facts(original_file, humanized_file):
    try:
        with open(original_file, 'r') as f1, open(humanized_file, 'r') as f2:
            original = f1.read()
            humanized = f2.read()

        orig_nums = extract_numbers(original)
        hum_nums = extract_numbers(humanized)

        missing = orig_nums - hum_nums
        added = hum_nums - orig_nums

        if missing:
            print(f"ERROR: Facts missing in humanized text: {missing}")
            return False

        # We don't necessarily error on added numbers, but warn
        if added:
            print(f"WARNING: Numbers added in humanized text: {added}")

        print("SUCCESS: All numerical facts preserved.")
        return True

    except Exception as e:
        print(f"Error checking facts: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_facts.py <original_file> <humanized_file>")
        sys.exit(1)
    success = check_facts(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
