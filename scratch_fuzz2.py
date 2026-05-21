import sys
sys.path.append('d:/command')
from rapidfuzz import process, fuzz
from dictionary import MAPPING

MAPPING_KEYS = list(MAPPING.keys())

tests = [
    "gar wall rifles",
    "gumball rifles",
    "have elder",
    "havel dar",
    "seek light infantry",
    "subbed our major",
    "report to"  # To test false positives
]

print("Using fuzz.ratio:")
for t in tests:
    match = process.extractOne(t, MAPPING_KEYS, scorer=fuzz.ratio)
    if match:
        print(f"'{t}' -> '{match[0]}' (Score: {match[1]:.2f})")

print("\nUsing default WRatio:")
for t in tests:
    match = process.extractOne(t, MAPPING_KEYS)
    if match:
        print(f"'{t}' -> '{match[0]}' (Score: {match[1]:.2f})")
