import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python flag_changes.py <original> <humanized>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        orig = f.read()
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        hum = f.read()

    orig_len = len(orig)
    hum_len = len(hum)

    if orig_len == 0:
        print("Error: Original file is empty.")
        sys.exit(1)

    change_ratio = hum_len / orig_len
    print(f"Original length: {orig_len} characters")
    print(f"Humanized length: {hum_len} characters")
    print(f"Change ratio: {change_ratio:.2f}")

    if change_ratio < 0.3:
        print("Warning/Fail: Humanized text is less than 30% of original length. You might have removed too much information.")
        sys.exit(1)
    elif change_ratio > 3.0: # allow larger ratio since humanized file includes 3 full drafts/sections
        print("Warning/Fail: Humanized text is more than 300% of original length. You might have added filler.")
        sys.exit(1)

    print("Pass: Length changes are within acceptable bounds.")
    sys.exit(0)

if __name__ == '__main__':
    main()