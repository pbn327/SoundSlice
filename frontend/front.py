import streamlit as st
import requests
import wave
import os

# Agregar CSS para la imagen de fondo desde un enlace y mejorar la apariencia
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/vector-gratis/fondo-pentagrama-musical-brillante-notas-sonido_1017-31220.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("SoundSplit - Separador de Canciones")

st.header("Procesar Música")
uploaded_file = st.file_uploader("Arrastra y suelta un archivo WAV", type=["wav"])

if uploaded_file:
    # Leer el contenido del archivo subido
    file_bytes = uploaded_file.read()

    # Guardar el archivo temporalmente para analizarlo
    temp_filename = f"temp_{uploaded_file.name}"
    with open(temp_filename, "wb") as temp_file:
        temp_file.write(file_bytes)

    # Obtener la duración del archivo WAV
    with wave.open(temp_filename, 'rb') as wave_file:
        frames = wave_file.getnframes()
        rate = wave_file.getframerate()
        duration = frames / float(rate)

    # Obtener el tamaño del archivo
    file_size = os.path.getsize(temp_filename) / (1024 * 1024)  # Convertir a MB

    # Mostrar la descripción del archivo
    st.write(f"Nombre del archivo: {uploaded_file.name}")
    st.write(f"Duración: {duration:.2f} segundos")
    st.write(f"Tamaño del archivo: {file_size:.2f} MB")

    st.success(f"Archivo '{uploaded_file.name}' subido correctamente.")

    # Botón para iniciar la separación de pistas
    if st.button("Separar pistas"):
        with st.spinner('Separando pistas...'):
            # Llamar a la API para separar las pistas
            response = requests.post('http://localhost:8000/separate', files={'wav_file': (uploaded_file.name, file_bytes, 'audio/wav')})
            if response.status_code == 200:
                st.success("Pistas separadas correctamente.")

                # Obtener URLs de las pistas
                track_urls = response.json().get("track_urls", [])

                if track_urls:
                    # Mostrar los reproductores de audio para cada pista
                    for track_name in ["bass.wav", "drums.wav", "other.wav", "vocals.wav"]:
                        track_url = f'http://localhost:8000/track/{track_name}'
                        st.audio(track_url)

                else:
                    st.error("No se encontraron pistas separadas.")

            else:
                st.error("Error al separar las pistas")

    # Eliminar el archivo temporal
    os.remove(temp_filename)
