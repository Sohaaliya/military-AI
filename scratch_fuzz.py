import sys
sys.path.append('d:/command')
from rapidfuzz import process
from dictionary import MAPPING

MAPPING_KEYS = list(MAPPING.keys())

tests = [
    "gar wall rifles",
    "gumball rifles",
    "have elder",
    "havel dar",
    "seek light infantry",
    "richmond",
    "stupid heart major",
    "subbed our major"
]

for t in tests:
    match = process.extractOne(t, MAPPING_KEYS)
    if match:
        print(f"'{t}' -> '{match[0]}' (Score: {match[1]:.2f}) -> {MAPPING[match[0]]}")
