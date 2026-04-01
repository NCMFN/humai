import sys
import statistics
import re

def get_sentences(paragraph):
    # Split by '.', '!', '?'
    sentences = re.split(r'(?<=[.!?])\s+', paragraph.strip())
    # Remove empty strings
    return [s for s in sentences if s.strip()]

def get_paragraphs(text):
    return [p for p in text.split('\n\n') if p.strip()]

def get_first_words(paragraphs):
    first_words = []
    for p in paragraphs:
        sentences = get_sentences(p)
        if sentences:
            first_words.append(sentences[0].split()[0].lower())
    return first_words

def calculate_lexical_diversity(first_words):
    if not first_words:
        return 1.0
    unique_words = set(first_words)
    return len(unique_words) / len(first_words)

def main():
    if len(sys.argv) != 3:
        print("Usage: python measure_readability.py <original_file> <humanized_file>")
        sys.exit(1)

    humanized_file = sys.argv[2]

    with open(humanized_file, 'r') as f:
        text = f.read()

    # Need to extract only the "Final rewrite" part for readability checks if multiple sections exist
    if "Final rewrite" in text:
        text_to_check = text.split("Final rewrite")[-1]
    else:
        text_to_check = text

    paragraphs = get_paragraphs(text_to_check)

    fail = False
    for i, paragraph in enumerate(paragraphs):
        sentences = get_sentences(paragraph)
        if not sentences:
            continue
        lengths = [len(s.split()) for s in sentences]
        if len(lengths) > 1:
            std_dev = statistics.stdev(lengths)
            if std_dev < 7:
                print(f"FAIL: Sentence length standard deviation in paragraph {i+1} is {std_dev:.2f} (must be >= 7).")
                fail = True

    first_words = get_first_words(paragraphs)
    diversity = calculate_lexical_diversity(first_words)

    if diversity < 0.8:
        print(f"FAIL: Paragraph-opening lexical diversity is {diversity*100:.1f}% (must be >= 80%).")
        fail = True

    if fail:
        sys.exit(1)
    else:
        print("PASS: Readability Metrics.")
        sys.exit(0)

if __name__ == "__main__":
    main()
