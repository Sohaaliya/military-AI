from faster_whisper import WhisperModel

model = WhisperModel("medium", device="cuda", compute_type="float16")

print("Transcribing with faster-whisper (no prompt)...")
segments, info = model.transcribe(
    "d:/command/input.wav",
    language="en",
    temperature=0.0,
    beam_size=5,
    condition_on_previous_text=False
)
text = " ".join([segment.text for segment in segments])
print("Result without prompt:", repr(text))
