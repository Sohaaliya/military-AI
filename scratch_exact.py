import sys
sys.path.append('d:/command')
import re
from dictionary import MAPPING

def resolve_text_exact_only(text):
    text = text.lower()
    text = re.sub(r"[^\w\s/]", "", text)
    words = text.split()
    result = []
    i = 0
    max_phrase_length = 5

    while i < len(words):
        matched = False
        for size in range(max_phrase_length, 0, -1):
            if i + size <= len(words):
                phrase = " ".join(words[i:i+size])
                if phrase in MAPPING:
                    result.append(MAPPING[phrase])
                    i += size
                    matched = True
                    break
        
        if not matched:
            result.append(words[i])
            i += 1

    final_text = " ".join(result)
    cleanup_rules = {
        "li light infantry": "li",
        "rif rifles": "rif",
        "regt regiment": "regt",
        "div division": "div",
        "co commanding officer": "co",
    }
    for wrong, correct in cleanup_rules.items():
        final_text = final_text.replace(wrong, correct)

    tokens = final_text.split()
    cleaned = []
    for word in tokens:
        if len(cleaned) == 0 or cleaned[-1] != word:
            cleaned.append(word)

    return " ".join(cleaned)

tests = [
    "everybody come to army postal service",
    "all report to one armoured regiment",
    "havildar report to 3 infantry division"
]

for t in tests:
    print(f"Original: '{t}' -> Resolved: '{resolve_text_exact_only(t)}'")
