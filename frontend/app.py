import streamlit as st

st.title("SoundSlice - Separador de Canciones")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

youtube_link = st.text_input("Introduce el enlace de YouTube")

uploaded_file = st.file_uploader("Sube un archivo MP3", type=["mp3"])

if youtube_link:
    st.write(f"Enlace de YouTube introducido: {youtube_link}")

if uploaded_file:
    st.write(f"Archivo subido: {uploaded_file.name}")

if youtube_link or uploaded_file:
    st.write("Procesando el audio...")
