import re
import sys
import numpy as np

def measure_readability(text):
    # Split text into paragraphs based on double newlines
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    # Analyze each paragraph
    sentence_lengths = []
    paragraph_openings = []

    for paragraph in paragraphs:
        # Simple sentence tokenizer based on periods, question marks, exclamation marks
        # (Does not handle abbreviations perfectly like "e.g.", "i.e.")
        sentences = re.split(r'[.!?]+', paragraph)
        sentences = [s.strip() for s in sentences if s.strip()]

        if sentences:
            # Word count for each sentence
            lengths = [len(re.findall(r'\b\w+\b', s)) for s in sentences]
            sentence_lengths.extend(lengths)

            # Paragraph opening
            first_sentence = sentences[0]
            words = re.findall(r'\b\w+\b', first_sentence)
            if words:
                paragraph_openings.append(words[0].lower())

    return sentence_lengths, paragraph_openings

def main():
    if len(sys.argv) != 3:
        print("Usage: python measure_readability.py <original_file> <humanized_file>")
        sys.exit(1)

    humanized_file = sys.argv[2]

    with open(humanized_file, 'r', encoding='utf-8') as f:
        humanized_text = f.read()

    if "Final rewrite" in humanized_text:
        humanized_text = humanized_text.split("Final rewrite")[1]

    lengths, openings = measure_readability(humanized_text)

    if not lengths:
        print("Readability metrics: Could not extract sentences.")
        sys.exit(1)

    avg_length = np.mean(lengths)
    std_dev = np.std(lengths)

    if len(openings) > 0:
        unique_openings = len(set(openings))
        lexical_diversity = unique_openings / len(openings) * 100
    else:
        lexical_diversity = 0

    print(f"Average sentence length: {avg_length:.2f} words")
    print(f"Sentence length standard deviation: {std_dev:.2f} words")
    print(f"Paragraph-opening lexical diversity: {lexical_diversity:.2f}%")

    if std_dev < 5.0:
        print("Readability and Rhythm Audit: FAILED (Standard deviation falls below 5 words, indicating monotony)")
        sys.exit(1)
    else:
        print("Readability and Rhythm Audit: PASSED")
        sys.exit(0)

if __name__ == "__main__":
    main()
