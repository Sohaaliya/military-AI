import sys
sys.path.append('d:/command')
from rapidfuzz import process, fuzz
from dictionary import MAPPING

VOCAB = list(set(MAPPING.keys()) | set(MAPPING.values()))

tests = ["three", "two", "want", "wants"]

for t in tests:
    match = process.extractOne(t, VOCAB)
    if match:
        print(f"'{t}' -> '{match[0]}' (Score: {match[1]:.2f})")
