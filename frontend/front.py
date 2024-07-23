import streamlit as st
import os
import requests

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
        st.success("Pistas separadas correctamente.")

        zip_filename = response.json().get('zip_filename')
        zip_file_url = f'http://localhost:8000/download/{zip_filename}'

        st.markdown(f"[Descargar archivo ZIP]({zip_file_url})", unsafe_allow_html=True)
    else:
        st.error("Hubo un error al procesar la canción.")
