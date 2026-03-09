import sys
import re
import statistics

def measure_readability(file_path):
    try:
        with open(file_path, 'r') as f:
            text = f.read()

        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        word_counts = []
        for s in sentences:
            words = re.findall(r'\b\w+\b', s)
            if words:
                word_counts.append(len(words))

        if not word_counts:
            print("No valid sentences found.")
            return False

        avg_length = statistics.mean(word_counts)
        variance = statistics.variance(word_counts) if len(word_counts) > 1 else 0.0

        print(f"Readability Metrics for {file_path}:")
        print(f"  Sentence count: {len(sentences)}")
        print(f"  Word count: {sum(word_counts)}")
        print(f"  Average sentence length: {avg_length:.2f} words")
        print(f"  Sentence length variance: {variance:.2f}")

        # Check for natural rhythm (variance is good)
        if variance < 10.0 and len(sentences) > 5:
            print("WARNING: Sentence lengths are highly uniform (low variance), indicating possible robotic cadence.")
        else:
            print("SUCCESS: Sentence length variance suggests natural rhythm.")

        return True

    except Exception as e:
        print(f"Error measuring readability: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python measure_readability.py <file_path>")
        sys.exit(1)
    success = measure_readability(sys.argv[1])
    sys.exit(0 if success else 1)
