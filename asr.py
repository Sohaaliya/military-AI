import whisper
model = whisper.load_model("small") 

def transcribe(audio_path):
    result = model.transcribe(
        audio_path,
        language="en",
        temperature=0,        
        best_of=3             
    )
    return result["text"].lower()