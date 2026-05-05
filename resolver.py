import re
from dictionary import MAPPING

def resolve_text(text):
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)

    words = text.split()
    result = []

    i = 0
    while i < len(words):
        matched = False

        
        for size in [3, 2, 1]:
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

    return " ".join(result)