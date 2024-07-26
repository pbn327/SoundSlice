from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
import os
import shutil
from API.utils import separate_tracks, extract_filename

app = FastAPI()

# Ruta donde se almacenan los archivos separados
SEPARATED_FILES_PATH = "API/separated_files"
UPLOADS_PATH = "API/uploaded_files"

# Asegúrate de que las carpetas existen
os.makedirs(SEPARATED_FILES_PATH, exist_ok=True)
os.makedirs(UPLOADS_PATH, exist_ok=True)

@app.get("/")
def root():
    return {'greeting': 'hi there'}

@app.post('/separate')
async def separate_file(wav_file: UploadFile = File(...)):
    local_filename = os.path.join(UPLOADS_PATH, 'cancion_bonita.wav')

    # Guardar el archivo en la carpeta de subidas
    with open(local_filename, "wb") as f:
        shutil.copyfileobj(wav_file.file, f)

    # Separar las pistas
    separate_tracks(local_filename, SEPARATED_FILES_PATH)
    song_name = extract_filename(local_filename)
    output_directory = os.path.join(SEPARATED_FILES_PATH, song_name)

    # Obtener los nombres de las pistas
    track_files = [f for f in os.listdir(output_directory) if os.path.isfile(os.path.join(output_directory, f))]
    track_urls = [f"/track/{track}" for track in track_files]

    return {"track_urls": track_urls}


@app.get('/track/{track_name}')
def get_track(track_name: str):
    # Asegúrate de usar el nombre de la canción correcto aquí
    song_name = "cancion_bonita"
    track_path = os.path.join(SEPARATED_FILES_PATH, song_name, track_name)
    print(track_path)
    # Verifica si el archivo existe
    if not os.path.isfile(track_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Devuelve el archivo de pista
    return FileResponse(track_path, media_type='audio/wav')
