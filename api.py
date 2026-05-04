from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil

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
    file_path = "temp.wav"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = transcribe(file_path)
    text = normalize(text)
    final = resolve_text(text)

    return {"output": final}