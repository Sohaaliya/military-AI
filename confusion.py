CONFUSION_SET = {
    "core": ["corps"],
    "corps": ["core"]
}

def has_confusion(words):
    return any(w in CONFUSION_SET for w in words)

def get_candidates(word):
    return CONFUSION_SET.get(word, [])