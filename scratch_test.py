import sys
import os
sys.path.append('d:/command')
from normalize import normalize
from resolver import resolve_text

test_text = "l nk come to electronics and mechanical engineering"
norm_text = normalize(test_text)
final_text = resolve_text(norm_text)

print("Original:", test_text)
print("Normalized:", norm_text)
print("Resolved:", final_text)
