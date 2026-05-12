import whisper

model = whisper.load_model("medium").to("cuda")


def transcribe(audio_path):

    result = model.transcribe(
        audio_path,

        language="en",

        temperature=0,

        beam_size=3,

        best_of=3,

        fp16=True,

        initial_prompt="""
        Military communication involving
        lieutenant general,
        regiment,
        division,
        corps,
        infantry,
        gorkha rifles,
        commanding officer,
        report immediately,
        forward ordnance depot,
        counter insurgency force,
        adjutant,
        maratha light infantry,
        sikh light infantry
        """
    )

    return result["text"].lower()