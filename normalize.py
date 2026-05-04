from rapidfuzz import process
import re
from dictionary import MAPPING

# Build vocabulary (keys + values)
VOCAB = list(set(MAPPING.keys()) | set(MAPPING.values()))


# 🔹 Handle simple plurals
def fix_plural(word):
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word


def normalize(text):
    # 🔹 Lowercase
    text = text.lower()

    # 🔹 Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    words = text.split()
    result = []

    for word in words:
        # 🔹 Handle plural
        word = fix_plural(word)

        # 🔹 Fuzzy match
        match = process.extractOne(word, VOCAB)

        if match:
            best_match, score, _ = match

            if score > 80:   # 🔥 tune this if needed
                result.append(best_match)
            else:
                result.append(word)
        else:
            result.append(word)

    return " ".join(result)