import re

def fix_missing_to(text):
    # Fix transcribed '2'
    text = re.sub(r'\b(report|come|go|return|send|talk)\s+2\b', r'\1 to', text)
    
    # Insert missing 'to' after movement verbs if the next word is not a preposition/adverb
    pattern = r'\b(report|come|go|return|send|talk)\s+(?!(to|2|immediately|back|away|out|in|on|at|for|with|and|the|a|an)\b)(\w+)'
    text = re.sub(pattern, r'\1 to \3', text)
    return text

tests = [
    "come eme",
    "report garhwal rifles",
    "go forward ordnance depot",
    "come to eme",
    "report immediately to 1/3 gr",
    "report 2 1/3 gr",
    "send reinforcements"
]

for t in tests:
    print(f"'{t}' -> '{fix_missing_to(t)}'")
