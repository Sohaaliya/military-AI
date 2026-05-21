import sys
sys.path.append('d:/command')
from normalize import normalize
from resolver import resolve_text

tests = [
    "want two three",
    "wants two three",
    "i want three"
]

for t in tests:
    n = normalize(t)
    r = resolve_text(n)
    print(f"Original: '{t}' -> Normalize: '{n}' -> Resolve: '{r}'")
