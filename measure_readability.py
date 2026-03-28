import sys
import re
import statistics

def count_words(sentence):
    return len(re.findall(r'\b\w+\b', sentence))

def main():
    if len(sys.argv) != 2:
        print("Usage: python measure_readability.py <humanized_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()

    # Split roughly by punctuation (. ? !)
    sentences = [s.strip() for s in re.split(r'[.?!]+', text) if s.strip()]

    if not sentences:
        print("Error: No sentences found.")
        sys.exit(1)

    lengths = [count_words(s) for s in sentences]

    mean_len = statistics.mean(lengths)
    stdev = statistics.stdev(lengths) if len(lengths) > 1 else 0

    print(f"Readability Metrics:")
    print(f"Average sentence length: {mean_len:.1f} words")
    print(f"Standard deviation (variation): {stdev:.1f} words")

    if stdev < 2.0:
        print("Warning/Fail: Low sentence variation detected. Text may sound monotonous/robotic.")
        sys.exit(1)

    print("Pass: Sentence variation is acceptable.")
    sys.exit(0)

if __name__ == '__main__':
    main()