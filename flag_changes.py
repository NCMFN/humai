import sys
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: python flag_changes.py <original_file> <humanized_file>")
        sys.exit(1)

    original_file = sys.argv[1]
    humanized_file = sys.argv[2]

    with open(original_file, 'r') as f:
        original_text = f.read()

    with open(humanized_file, 'r') as f:
        humanized_text = f.read()

    original_len = len(original_text.split())
    humanized_len = len(humanized_text.split())

    if original_len == 0:
        ratio = 0
    else:
        ratio = humanized_len / original_len

    print(f"Original length: {original_len} words")
    print(f"Humanized length: {humanized_len} words")
    print(f"Change Ratio: {ratio:.2f}")

    if ratio > 3.0:
        print("FAIL: The humanized output exceeds the maximum change ratio of 3.0.")
        sys.exit(1)
    else:
        print("PASS: Change Threshold Check.")
        sys.exit(0)

if __name__ == "__main__":
    main()
