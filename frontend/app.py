import streamlit as st
import re
import requests
from PIL import Image
from io import BytesIO

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

## Función para validar el enlace de YouTube
def is_valid_youtube_link(link):
    youtube_regex = r'^(https?://)?(www\.)?youtube\.com/(watch\?v=|embed/|v/|user\/.+\?v=|[^/]+\?v=)([a-zA-Z0-9_-]{11}).*$'
    return bool(re.match(youtube_regex, link))

## Función para obtener la miniatura de YouTube
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
    uploaded_file = st.file_uploader("Arrastra y suelta un archivo MP3", type=["mp3"])
    if uploaded_file:
        st.write(f"Archivo subido: {uploaded_file.name}")

## Segunda sección: Pistas Disponibles y Sube tus Pistas
with col2:
    st.header("Pistas Disponibles")
    # Aquí se generarían las 5 pistas después de procesar la música
    selected_tracks = []
    for i in range(1, 6):
        if st.checkbox(f"Pista {i}"):
            selected_tracks.append(f"Contenido de la pista {i}")

    if selected_tracks:
        st.download_button(
            label="Descargar Pistas Seleccionadas",
            data="\n".join(selected_tracks),
            file_name="pistas_seleccionadas.zip",
            mime="application/zip",
        )

    st.header("Sube tus Pistas")
    uploaded_files = st.file_uploader("Arrastra y suelta tus pistas", type=["mp3"], accept_multiple_files=True)
    if uploaded_files:
        st.write(f"Has subido {len(uploaded_files)} pistas.")
    else:
        st.write("Aún no has subido tus pistas.")
