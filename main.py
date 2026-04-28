import joblib
from asr import transcribe
from confusion import has_confusion, get_candidates
from preprocess import get_window
from embed import encode
from resolver import resolve

# load trained model once
model = joblib.load("trained_model.pkl")

def process(audio_path):
    text = transcribe(audio_path)

    words = text.split()

    # ⚡ FAST EXIT (very important)
    if not has_confusion(words):
        return text

    for i, w in enumerate(words):
        candidates = get_candidates(w)

        if candidates:
            # ⚡ use small context window
            context = get_window(words, i)

            vec = encode(context)

            prediction = model.predict(vec)

            words = resolve(words, i, prediction)

    return " ".join(words)


if __name__ == "__main__":
    audio_file = "sample.wav"
    output = process(audio_file)
    print("FINAL:", output)