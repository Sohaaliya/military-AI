from asr import transcribe
from normalize import normalize
from resolver import resolve_text
from mic import record_audio

def speech_to_command(audio_file):
    """
    Full pipeline:
    Audio → ASR → Normalize → Resolve → Final text
    """
    # Step 1: Speech to text
    text = transcribe(audio_file)

    # Step 2: Normalize common ASR mistakes
    text = normalize(text)

    # Step 3: Apply dictionary corrections
    final_text = resolve_text(text)

    return final_text


if __name__ == "__main__":
    # Input audio file
    audio_file = record_audio()

    # Process and get final corrected output
    output = speech_to_command(audio_file)

    # ✅ Only final corrected text is displayed
    print(output)