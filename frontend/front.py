import streamlit as st
import os
import requests
from io import BytesIO
import zipfile

# Ruta donde se guardarán los archivos subidos
UPLOADS_PATH = "/home/luis/code/pbn327/SoundSlice/frontend/uploaded_files"
SEPARATED_FILES_PATH = "/home/luis/code/pbn327/SoundSlice/frontend/separated_files"

st.markdown(
    """
    <style>
    .stApp {
        background-color: #8B5FBF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("SoundSlice - Separador de Canciones")

st.header("Procesar Música")
uploaded_file = st.file_uploader("Arrastra y suelta un archivo WAV", type=["wav"])

if uploaded_file:
    # Guardar el archivo en la carpeta de subidas
    file_path = os.path.join(UPLOADS_PATH, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Archivo '{uploaded_file.name}' subido correctamente.")

    # Llamar a la API para separar las pistas
    response = requests.post('http://localhost:8000/separate', json={'wav_file': uploaded_file.name})
    if response.status_code == 200:
        st.success("Pistas separadas correctamente. Selecciona las pistas para descargar.")
    else:
        st.error("Hubo un error al procesar la canción.")

    st.header("Pistas Disponibles")
    track_folder = uploaded_file.name.replace('.wav', '')
    track_folder_path = os.path.join(SEPARATED_FILES_PATH, track_folder)

    # Nombres de las pistas esperadas
    expected_tracks = ["bass.wav", "drums.wav", "other.wav", "vocals.wav"]

#los archivos son buscados antes de ser generados por el modelo, no es error sino bug


    # Verificar que las pistas existen en la carpeta
    # if os.path.exists(track_folder_path):
    #     print("probando1")
    #     track_files = [f for f in expected_tracks if os.path.isfile(os.path.join(track_folder_path, f))]
    #     selected_tracks = []

    #     for track_file in track_files:
    #         if st.checkbox(track_file):
    #             selected_tracks.append(os.path.join(track_folder_path, track_file))

    #     print("probando2")
    #     # En la sección de descarga de pistas seleccionadas
    #     if selected_tracks:
    #         print("probando3")
    #         zip_path = os.path.join(SEPARATED_FILES_PATH, f"{track_folder}_selected_tracks.zip")

    #         with zipfile.ZipFile(zip_path, 'w') as zipf:
    #             print("probando4")
    #             for file in selected_tracks:
    #                 zipf.write(file, os.path.basename(file))

    #         with open(zip_path, 'rb') as f:
    #             print("probando5")
    #             st.download_button(
    #                 label="Descargar Pistas Seleccionadas",
    #                 data=f.read(),
    #                 file_name=f"{track_folder}_selected_tracks.zip",
    #                 mime="application/zip",
    #             )
    #     else:
    #         st.write("Selecciona las pistas que deseas descargar.")
