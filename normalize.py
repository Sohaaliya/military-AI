import re
from rapidfuzz import process
from dictionary import MAPPING

VOCAB = list(set(MAPPING.keys()) | set(MAPPING.values()))

# 🔥 FIX 1: numeric patterns
def fix_numbers(text):
    # 1x3 or 1 x 3 → 1/3
    text = re.sub(r'(\d)\s*x\s*(\d)', r'\1/\2', text)

    # 🔥 NEW: "13 gorkha rifles" → "1/3 gorkha rifles"
    text = re.sub(r'\b13\s+(gorkha rifles)\b', r'1/3 \1', text)

    return text

# 🔥 FIX 2: joined words
def fix_joined_words(text):
    text = text.replace("counterinsurgency", "counter insurgency")
    return text

# 🔥 OPTIONAL: plural fix
def fix_plural(word):
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word


def normalize(text):
    text = text.lower()

    # ✅ APPLY EARLY (IMPORTANT)
    text = fix_numbers(text)
    text = fix_joined_words(text)

    # clean punctuation but keep /
    text = re.sub(r'[^\w\s/]', '', text)

    words = text.split()
    result = []

    for word in words:
        original = word
        word = fix_plural(word)

        match = process.extractOne(word, VOCAB)

        if match:
            best_match, score, _ = match

            # 🔥 STRICT matching (avoid wrong corrections)
            if score > 90:
                result.append(best_match)
            else:
                result.append(original)
        else:
            result.append(original)

    return " ".join(result)