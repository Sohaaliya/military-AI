import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import noisereduce as nr

def record_audio(filename="input.wav", duration=10, fs=16000):
    print("🎙️ Speak clearly...")

    recording = sd.rec(
        int(duration * fs),
        samplerate=fs,
        channels=1,
        dtype='float32'
    )
    sd.wait()

    audio_data = recording.flatten()
    
    # Safely normalize without clipping
    # Only amplify if there's actual signal (max volume > 2%)
    max_val = np.max(np.abs(audio_data))
    if max_val > 0.02:
        audio_data = audio_data / max_val
    
    # Ensure float limits
    audio_data = np.clip(audio_data, -1.0, 1.0)
    
    # Convert to 16-bit PCM
    audio_data_int16 = (audio_data * 32767).astype(np.int16)

    write(filename, fs, audio_data_int16)

    print("✅ Recording saved")
    return filename