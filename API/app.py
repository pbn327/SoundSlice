from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
import os
import zipfile
from API.utils import separate_tracks, extract_filename
import shutil

app = FastAPI()

# Ruta donde se almacenan los archivos separados
SEPARATED_FILES_PATH = "API/separated_files"
UPLOADS_PATH = "API/uploaded_files"

@app.get("/")
def root():
    return {'greeting': 'Hello'}

@app.post('/separate')
async def separate_file(wav_file: UploadFile = File(...)): #.wav como argumento
    local_filename = 'API/uploaded_files/cancion_bonita.wav'

    # Guardar el archivo en la carpeta de subidas
    with open(local_filename, "wb") as f:
        shutil.copyfileobj(wav_file.file, f)

    # Separar las pistas
    separate_tracks(local_filename, SEPARATED_FILES_PATH)
    output_directory = os.path.join(SEPARATED_FILES_PATH, extract_filename(local_filename))
    #nombre del zip
    zip_filename = f"{extract_filename(local_filename)}_separated.zip"
    #zipear lo que se encuentre en esta ubicación
    zip_file_path = os.path.join(SEPARATED_FILES_PATH, zip_filename)

    # Crear el archivo ZIP usando zipfile
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for root, _, files in os.walk(output_directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_directory)
                zipf.write(file_path, arcname=arcname)

    #return {"detail": "Separation done", "zip_filename": zip_filename}
    return FileResponse(path=zip_file_path,filename=zip_filename)

@app.get('/download/{filename}')
def download_file(filename:str):
    file_path=os.path.join(SEPARATED_FILES_PATH,filename)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return StreamingResponse(open(file_path, 'rb'), media_type='application/zip', headers={'Content-Disposition': f'attachment; filename="{filename}"'})
