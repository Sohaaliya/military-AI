from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
import noisereduce as nr
from scipy.io import wavfile
import numpy as np

from asr import transcribe
from normalize import normalize
from resolver import resolve_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    raw_path = "temp.webm"
    file_path = "temp.wav"

    with open(raw_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        import subprocess
        # Convert webm to 16kHz PCM WAV
        subprocess.run(["ffmpeg", "-y", "-i", raw_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        fs, data = wavfile.read(file_path)
        
        # Safely normalize without clipping (max volume > 2%)
        max_val = np.max(np.abs(data))
        if max_val > 0.02:
            data_float = data.astype(np.float32) / max_val
            data_float = np.clip(data_float, -1.0, 1.0)
            data = (data_float * 32767).astype(np.int16)
            
        wavfile.write(file_path, fs, data)
    except Exception as e:
        print(f"Warning: Audio processing skipped - {e}")
        # Fallback if ffmpeg fails: just pass raw_path
        file_path = raw_path

    text = transcribe(file_path)
    print(f"DEBUG API ASR Output: '{text}'")
    text = normalize(text)
    print(f"DEBUG API Normalized Output: '{text}'")
    final = resolve_text(text)
    print(f"DEBUG API Final Output: '{final}'")

    return {"output": final}