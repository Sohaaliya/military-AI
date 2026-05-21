import re
from rapidfuzz import process, fuzz
from dictionary import MAPPING

MAPPING_KEYS = list(MAPPING.keys())

def resolve_text(text):

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^\w\s/]", "", text)

    words = text.split()

    result = []
    KEEP_WORDS = {
    "to",
    "from",
    "at",
    "in",
    "on",
    "with",
    "and"
}
    i = 0

    # Try longest phrases first
    max_phrase_length = 5

    while i < len(words):

        matched = False

        # Check 5-word → 1-word phrases
        for size in range(max_phrase_length, 0, -1):

            if i + size <= len(words):

                phrase = " ".join(words[i:i+size])

                # 1. Exact match
                if phrase in MAPPING:
                    result.append(MAPPING[phrase])
                    i += size
                    matched = True
                    break
                
                # 2. Safe Phrase Fuzzy Match (fuzz.ratio prevents false positives)
                if len(phrase) >= 5:
                    match = process.extractOne(phrase, MAPPING_KEYS, scorer=fuzz.ratio)
                    if match:
                        best_match, score, _ = match
                        # Catch exact phonetic similarities without scrambling non-military words
                        if score >= 80:
                            result.append(MAPPING[best_match])
                            i += size
                            matched = True
                            break

        # No match found
        if not matched:
            result.append(words[i])
            i += 1

    final_text = " ".join(result)

    # -------------------------
    # Cleanup duplicate phrases
    # -------------------------

    cleanup_rules = {
        "li light infantry": "li",
        "rif rifles": "rif",
        "regt regiment": "regt",
        "div division": "div",
        "co commanding officer": "co",
    }

    for wrong, correct in cleanup_rules.items():
        final_text = final_text.replace(wrong, correct)

    # Remove repeated consecutive words
    tokens = final_text.split()

    cleaned = []

    for word in tokens:
        if len(cleaned) == 0 or cleaned[-1] != word:
            cleaned.append(word)

    final_text = " ".join(cleaned)

    return final_text