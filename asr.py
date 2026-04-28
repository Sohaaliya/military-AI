import whisper

# Use tiny for speed (change to base if needed)
model = whisper.load_model("tiny")

def transcribe(audio_path):
    result = model.transcribe(audio_path)
    return result["text"].lower()