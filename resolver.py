import re
from dictionary import MAPPING

def resolve_text(text):

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^\w\s/]", "", text)

    words = text.split()

    result = []
    i = 0

    # Try longest phrases first
    max_phrase_length = 5

    while i < len(words):

        matched = False

        # Check 5-word → 1-word phrases
        for size in range(max_phrase_length, 0, -1):

            if i + size <= len(words):

                phrase = " ".join(words[i:i+size])

                if phrase in MAPPING:

                    replacement = MAPPING[phrase]

                    result.append(replacement)

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