import streamlit as st
import os
import requests

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
    # Leer el contenido del archivo subido

    file_bytes=uploaded_file.read()

    st.success(f"Archivo '{uploaded_file.name}' subido correctamente.")

    # Llamar a la API para separar las pistas
    with requests.post('http://localhost:8000/separate', files={'wav_file': ('cancion_bonita.wav', file_bytes, 'audio/wav')},stream=True) as response:
        if response.status_code == 200:
            # with open('cancion.zip','wb') as f:
            #     f.write(response.content)
            st.success("Pistas separadas correctamente.")

            #zip_filename = response.json().get('zip_filename')
            st.download_button(label="Descargar archivo ZIP",
                               data=response.content,
                               file_name=f"audios_separados.zip",
                               mime='application/zip')
        else:
            st.error("NO SE RECIBIÓ EL ARCHIVO ")
