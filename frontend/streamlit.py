import streamlit as st
import os
import requests
from io import BytesIO

# Ruta donde se guardarán los archivos subidos
UPLOADS_PATH = "frontend/uploaded_files"
SEPARATED_FILES_PATH = "frontend/separated_files"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #8B5FBF;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.title("SoundSlice - Separador de Canciones")

## Regex para validar el enlace de YouTube
def is_valid_youtube_link(link):
    youtube_regex = r'^(https?://)?(www\.)?youtube\.com/(watch\?v=|embed/|v/|user\/.+\?v=|[^/]+\?v=)([a-zA-Z0-9_-]{11}).*$'
    return bool(re.match(youtube_regex, link))

## Miniatura de YouTube
def get_youtube_thumbnail(link):
    video_id = re.search(r'[?&]v=([^&]+)', link).group(1)
    thumbnail_url = f'https://img.youtube.com/vi/{video_id}/0.jpg'
    response = requests.get(thumbnail_url)
    return Image.open(BytesIO(response.content))

## Crear las secciones
col1, col2 = st.columns(2)

## Primera sección: Procesar Música
with col1:
    st.header("Procesar Música")
    youtube_link = st.text_input("Introduce el enlace de YouTube")
    if youtube_link:
        if is_valid_youtube_link(youtube_link):
            thumbnail = get_youtube_thumbnail(youtube_link)
            st.image(thumbnail, caption='Thumbnail de la canción')
        else:
            st.write("El enlace de YouTube no es válido.")
    uploaded_file = st.file_uploader("Arrastra y suelta un archivo WAV", type=["wav"])
    if uploaded_file:
        # Guardar el archivo en la carpeta de subidas
        file_path = os.path.join(UPLOADS_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Archivo '{uploaded_file.name}' subido correctamente.")

        # Llamar a la API para separar las pistas (esto es solo un ejemplo, asegúrate de que tu API esté correctamente configurada)
        response = requests.post(f'http://localhost:8000/separate', params={'wav_file': uploaded_file.name})
        if response.status_code == 200:
            st.success("Pistas separadas correctamente. Selecciona las pistas para descargar.")
        else:
            st.error("Hubo un error al procesar la canción.")

## Segunda sección: Pistas Disponibles y Subir Más Pistas
with col2:
    st.header("Pistas Disponibles")
    track_folder = "track3"  # Ajusta esto para que coincida con el nombre de la pista subida
    track_folder_path = os.path.join(SEPARATED_FILES_PATH, track_folder)

    # Nombres de las pistas esperadas
    expected_tracks = ["bass.wav", "drums.wav", "other.wav", "vocals.wav"]

    # Verificar que las pistas existen en la carpeta
    if os.path.exists(track_folder_path):
        track_files = [f for f in expected_tracks if os.path.isfile(os.path.join(track_folder_path, f))]
        selected_tracks = []

        for track_file in track_files:
            if st.checkbox(track_file):
                selected_tracks.append(os.path.join(track_folder_path, track_file))

        if selected_tracks:
            st.download_button(
                label="Descargar Pistas Seleccionadas",
                data=b''.join(open(file, 'rb').read() for file in selected_tracks),
                file_name="pistas_seleccionadas.zip",
                mime="application/zip",
            )
        else:
            st.write("Selecciona las pistas que deseas descargar.")

    st.header("Sube tus Pistas")
    uploaded_files = st.file_uploader("Arrastra y suelta tus pistas", type=["wav"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Guardar cada archivo en la carpeta de subidas
            file_path = os.path.join(UPLOADS_PATH, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        st.success(f"Has subido {len(uploaded_files)} pistas.")
    else:
        st.write("Aún no has subido tus pistas.")
