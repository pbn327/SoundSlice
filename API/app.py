from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import os
import zipfile
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

    # Separar las pistas
    separate_tracks(file_path, SEPARATED_FILES_PATH)

    output_directory = os.path.join(SEPARATED_FILES_PATH, extract_filename(wav_file))
    zip_filename = f"{extract_filename(wav_file)}_separated.zip"
    zip_file_path = os.path.join(SEPARATED_FILES_PATH, zip_filename)

    # Crear el archivo ZIP usando zipfile
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(output_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_directory)
                zipf.write(file_path, arcname=arcname)

    return {"detail": "Separation done", "output_directory": output_directory, "zip_filename": zip_filename}

@app.get('/download/{filename}')
def download_file(filename: str):
    file_path = os.path.join(SEPARATED_FILES_PATH, filename)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return StreamingResponse(open(file_path, 'rb'), media_type='application/zip', headers={'Content-Disposition': f'attachment; filename="{filename}"'})
