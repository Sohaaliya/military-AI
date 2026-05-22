from faster_whisper import WhisperModel

# Run on GPU with FP16
model = WhisperModel("medium", device="cuda", compute_type="float16")

def transcribe(audio_path):

    segments, info = model.transcribe(
        audio_path,
        language="en",
        temperature=0.0,
        beam_size=5,
        condition_on_previous_text=False, # Prevents hallucinations
        initial_prompt="rhm, chm, regimental havildar major, company havildar major, lieutenant general, subedar major, naib subedar, havildar, naik, sepoy, regiment, division, corps, infantry, gorkha rifles, commanding officer, report immediately, forward ordnance depot, counter insurgency force, adjutant, maratha light infantry, sikh light infantry"
    )

    text = " ".join([segment.text for segment in segments])
    return text.lower().strip()