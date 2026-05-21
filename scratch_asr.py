import sys
import os
sys.path.append('d:/command')
from asr import transcribe

print("Transcribing input.wav...")
text = transcribe("input.wav")
print("Transcribed text:", repr(text))
