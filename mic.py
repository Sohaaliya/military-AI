import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def record_audio(filename="input.wav", duration=10, fs=16000):
    print("🎙️ Speak clearly...")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype='float32'
    )
    sd.wait()

    
    max_val = np.max(np.abs(recording))
    if max_val > 0:
        recording = recording / max_val

    write(filename, fs, recording)

    print("✅ Recording saved")
    return filename