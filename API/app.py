from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from utils import separate_tracks, extract_filename

app = FastAPI()

# Ruta donde se almacenan los archivos separados
SEPARATED_FILES_PATH = "/home/luis/code/pbn327/SoundSlice/frontend/separated_files"
UPLOADS_PATH = "/home/luis/code/pbn327/SoundSlice/frontend/uploaded_files"

@app.post('/')
def index():
    return {'ok': True} #regresar el output del separate cuando el usuario hace post

@app.get('/separate')
def separate_file(wav_file: str):
    file_path = os.path.join(UPLOADS_PATH, wav_file)
    print(file_path,"base + name_file")

    #/home/luis/code/pbn327/SoundSlice/frontend/uploaded_files/
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Extraer el nombre base del archivo
    base_name = extract_filename(wav_file)
    print("nombre de la canción")
    print(base_name)

    # Directorio donde se almacenarán los archivos separados
    output_directory = os.path.join(SEPARATED_FILES_PATH, base_name)
    print("directorio con nombre de cancion")
    print(output_directory)
    if not os.path.exists(output_directory):
        print(f"Creando directorio {output_directory}")
        os.makedirs(output_directory)

    # Separar las pistas
    print(f"pasando argumentos {file_path} - {output_directory}")
    #separate_tracks(file_path, output_directory)
    wavfile_path='/home/luis/code/pbn327/SoundSlice/frontend/uploaded_files/track4.wav'
    separate_tracks(wavfile_path, output_directory)

    return {"detail": "Separation done", "output_directory": output_directory}
