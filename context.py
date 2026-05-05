# context.py

from rapidfuzz import process
from dictionary import MAPPING

# Build military vocabulary
MILITARY_VOCAB = list(set(MAPPING.keys()) | set(MAPPING.values()))

def is_military_context(text):
    words = text.lower().split()
    score = 0

    for word in words:
        match = process.extractOne(word, MILITARY_VOCAB)

        if match:
            _, similarity, _ = match

            if similarity > 85:
                score += 1

    # 🔥 threshold (tune this)
    return score >= 1