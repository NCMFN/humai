import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python flag_changes.py <original_file> <humanized_file>")
        sys.exit(1)

    original_file = sys.argv[1]
    humanized_file = sys.argv[2]

    with open(original_file, 'r', encoding='utf-8') as f:
        original_text = f.read()

    with open(humanized_file, 'r', encoding='utf-8') as f:
        humanized_text = f.read()

    orig_len = len(original_text)
    hum_len = len(humanized_text)

    # According to memory: appropriate output length allows up to a 3.0 change ratio to accommodate the multi-section output structure
    if orig_len == 0:
        ratio = 0
    else:
        ratio = hum_len / orig_len

    print(f"Original length: {orig_len} chars")
    print(f"Humanized length: {hum_len} chars")
    print(f"Change ratio: {ratio:.2f}")

    if ratio > 3.0:
        print("Drift Detection / Change Threshold: FAILED (Ratio > 3.0)")
        sys.exit(1)
    else:
        print("Drift Detection / Change Threshold: PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()
