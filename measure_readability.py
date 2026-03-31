import sys
import numpy as np
import re

if __name__ == '__main__':
    try:
        with open(sys.argv[2], 'r') as f:
            text = f.read()

        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        lengths = [len(s.split()) for s in sentences]

        if lengths:
            std_dev = np.std(lengths)
            print(f"Readability Check: std dev = {std_dev:.2f}")
            if std_dev < 5.0:
                print("WARNING: Sentence length monotony detected (std dev < 5.0).")
            elif std_dev >= 7.0:
                print("Readability Check: PASSED (std dev >= 7.0).")
            else:
                print("Readability Check: PASSED (but variance could be higher).")
        else:
            print("Readability Check: No sentences found.")
    except Exception as e:
        print(f"Error measuring readability: {e}")
