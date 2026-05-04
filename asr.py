import whisper
model = whisper.load_model("small") # or "small" for better accuracy

def transcribe(audio_path):
    result = model.transcribe(
        audio_path,
        language="en",
        temperature=0,        # 🔥 reduces random guesses
        best_of=3             # 🔥 picks best output
    )
    return result["text"].lower()