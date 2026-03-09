import sys
import re

def count_words(text):
    return len(re.findall(r'\b\w+\b', text))

def flag_changes(original_file, humanized_file):
    try:
        with open(original_file, 'r') as f1, open(humanized_file, 'r') as f2:
            original = f1.read()
            humanized = f2.read()

        orig_word_count = count_words(original)
        hum_word_count = count_words(humanized)

        if orig_word_count == 0:
            print("Original text is empty.")
            return False

        ratio = hum_word_count / orig_word_count
        print(f"Original word count: {orig_word_count}")
        print(f"Humanized word count: {hum_word_count}")
        print(f"Ratio: {ratio:.2f}")

        if ratio < 0.5:
            print("WARNING: Humanized text is less than 50% the length of the original. Did facts get dropped?")
            return False
        elif ratio > 1.5:
            print("WARNING: Humanized text is more than 150% the length of the original. Did AI invent new content?")
            return False
        else:
            print("SUCCESS: Output length is within acceptable bounds.")
            return True

    except Exception as e:
        print(f"Error flagging changes: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flag_changes.py <original_file> <humanized_file>")
        sys.exit(1)
    success = flag_changes(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
