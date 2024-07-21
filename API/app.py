from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from utils import extract_filename

app = FastAPI()

# Ruta donde se almacenan los archivos separados
SEPARATED_FILES_PATH = "frontend/separated_files"

class WavFileRequest(BaseModel):
    wav_file: str

@app.get('/')
def index():
    return {'ok': True}

@app.post('/separate')
def get_separated_files(request: WavFileRequest):
    # Extraer el nombre base del archivo
    base_name = extract_filename(request.wav_file)

    # Directorio donde se encuentran los archivos separados
    track_folder_path = os.path.join(SEPARATED_FILES_PATH, base_name)

    expected_files = ["bass.wav", "drums.wav", "other.wav", "vocals.wav"]
    files_to_return = []

    for file_name in expected_files:
        file_path = os.path.join(track_folder_path, file_name)
        if os.path.isfile(file_path):
            files_to_return.append(file_path)

    return {"files": [FileResponse(file) for file in files_to_return]}
