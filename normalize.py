import re
from rapidfuzz import process
from dictionary import MAPPING

# All valid military vocabulary
VOCAB = list(set(MAPPING.keys()) | set(MAPPING.values()))

# Protect normal English words from wrong military correction
PROTECTED_WORDS = {
    "core",
    "earth",
    "first",
    "fast",
    "strong",
    "system",
    "normal",
    "ready",
    "move",
    "ahead"
}


# -----------------------------
# FIX 1: numeric patterns
# -----------------------------
def fix_numbers(text):

    # 1x3 or 1 x 3 → 1/3
    text = re.sub(r'(\d)\s*x\s*(\d)', r'\1/\2', text)

    # 13 gorkha rifles → 1/3 gorkha rifles
    text = re.sub(
        r'\b13\s+(gorkha rifles)\b',
        r'1/3 \1',
        text
    )

    return text


# -----------------------------
# FIX 2: joined military words
# -----------------------------
def fix_joined_words(text):

    fixes = {
        "counterinsurgency": "counter insurgency",
        "counterinsurgencyforce": "counter insurgency force",
        "lightinfantry": "light infantry",
    }

    for wrong, correct in fixes.items():
        text = text.replace(wrong, correct)

    return text


# -----------------------------
# FIX 3: plural handling
# -----------------------------
def fix_plural(word):

    if word.endswith("s") and len(word) > 3:
        return word[:-1]

    return word


# -----------------------------
# MAIN NORMALIZATION
# -----------------------------
def normalize(text):

    text = text.lower()

    # Apply fixes early
    text = fix_numbers(text)
    text = fix_joined_words(text)

    # Remove punctuation but keep /
    text = re.sub(r"[^\w\s/]", "", text)

    words = text.split()

    result = []

    for word in words:

        original = word

        # Skip protected words
        if word in PROTECTED_WORDS:
            result.append(word)
            continue

        # Ignore very short words
        if len(word) <= 2:
            result.append(word)
            continue

        # Fix plural
        normalized_word = fix_plural(word)

        # Fuzzy match
        match = process.extractOne(
            normalized_word,
            VOCAB
        )

        if match:

            best_match, score, _ = match

            # Strict threshold
            if score >= 90:
                result.append(best_match)
            else:
                result.append(original)

        else:
            result.append(original)

    final_text = " ".join(result)

    # -----------------------------
    # Cleanup duplicate phrases
    # -----------------------------
    cleanup_rules = {
        "li light infantry": "li",
        "rif rifles": "rif",
        "regt regiment": "regt",
        "div division": "div",
        "co commanding officer": "co",
    }

    for wrong, correct in cleanup_rules.items():
        final_text = final_text.replace(wrong, correct)

    return final_text