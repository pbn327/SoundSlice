from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from utils import separate_tracks, extract_filename

app = FastAPI()

# Ruta donde se almacenan los archivos separados
SEPARATED_FILES_PATH = "/home/luis/code/pbn327/SoundSlice/frontend/separated_files"
UPLOADS_PATH = "/home/luis/code/pbn327/SoundSlice/frontend/uploaded_files"

class SeparateRequest(BaseModel):
    wav_file: str

@app.post('/separate')
def separate_file(request: SeparateRequest):
    wav_file = request.wav_file
    file_path = os.path.join(UPLOADS_PATH, wav_file)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Extraer el nombre base del archivo
    base_name = extract_filename(wav_file)
    output_directory = os.path.join(SEPARATED_FILES_PATH, base_name)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Separar las pistas
    separate_tracks(file_path, output_directory)

    return {"detail": "Separation done", "output_directory": output_directory}
