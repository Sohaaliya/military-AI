import re
from rapidfuzz import process
from dictionary import MAPPING

# ---------------------------------
# ALL VALID VOCABULARY
# ---------------------------------
VOCAB = list(set(MAPPING.keys()) | set(MAPPING.values()))

# ---------------------------------
# WORDS THAT SHOULD NEVER CHANGE
# ---------------------------------
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
    "ahead",
    "forward",
    "report",
    "quickly",
    "rapidly"
}

# ---------------------------------
# SHORT MILITARY ABBREVIATIONS
# DO NOT FUZZY MATCH THESE
# ---------------------------------
SHORT_FORMS = {
    "rhm",
    "co",
    "lo",
    "ms",
    "br",
    "nk",
    "lt",
    "gen",
    "fod",
    "mes",
    "asc",
    "aec",
    "aps",
    "div",
    "corps",
    "cif",
    "adm"
}

# ---------------------------------
# FIX 1: NUMERIC PATTERNS
# ---------------------------------
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


# ---------------------------------
# FIX 2: JOINED WORDS
# ---------------------------------
def fix_joined_words(text):

    fixes = {
        "counterinsurgency": "counter insurgency",
        "counterinsurgencyforce": "counter insurgency force",
        "lightinfantry": "light infantry",
    }

    for wrong, correct in fixes.items():
        text = text.replace(wrong, correct)

    return text


# ---------------------------------
# FIX 3: SIMPLE PLURAL HANDLING
# ---------------------------------
def fix_plural(word):

    if word.endswith("s") and len(word) > 4:
        return word[:-1]

    return word


# ---------------------------------
# MAIN NORMALIZATION
# ---------------------------------
def normalize(text):

    text = text.lower()

    # Apply preprocessing
    text = fix_numbers(text)
    text = fix_joined_words(text)

    # Remove punctuation but keep /
    text = re.sub(r"[^\w\s/]", "", text)

    words = text.split()

    result = []

    for word in words:

        original = word

        # ---------------------------------
        # Skip protected words
        # ---------------------------------
        if word in PROTECTED_WORDS:
            result.append(word)
            continue

        # ---------------------------------
        # Skip short abbreviations
        # ---------------------------------
        if word in SHORT_FORMS:
            result.append(word)
            continue

        # ---------------------------------
        # Ignore very short words
        # Prevent crazy fuzzy matching
        # ---------------------------------
        if len(word) <= 4:
            result.append(word)
            continue

        # ---------------------------------
        # Exact dictionary word exists
        # ---------------------------------
        if word in MAPPING:
            result.append(word)
            continue

        # ---------------------------------
        # Fix plural
        # ---------------------------------
        normalized_word = fix_plural(word)

        # ---------------------------------
        # Fuzzy matching
        # ---------------------------------
        match = process.extractOne(
            normalized_word,
            VOCAB
        )

        if match:

            best_match, score, _ = match

            # STRICT threshold
            if score >= 92:
                result.append(best_match)
            else:
                result.append(original)

        else:
            result.append(original)

    final_text = " ".join(result)

    # ---------------------------------
    # CLEANUP DUPLICATES
    # ---------------------------------
    cleanup_rules = {
        "li light infantry": "li",
        "rif rifles": "rif",
        "regt regiment": "regt",
        "div division": "div",
        "co commanding officer": "co",
        "auto tech automotive technician": "auto tech",
    }

    for wrong, correct in cleanup_rules.items():
        final_text = final_text.replace(wrong, correct)

    return final_text