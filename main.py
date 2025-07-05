from fastapi import FastAPI, UploadFile, File
import whisper
import tempfile
import shutil
import os

app = FastAPI()
model = whisper.load_model("small.en")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Transcribe the audio file using Whisper
    result = model.transcribe(tmp_path)
    os.remove(tmp_path)  # Clean up the temporary file
    return {"text": result["text"]}
