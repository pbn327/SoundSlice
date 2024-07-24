from spleeter.separator import Separator
from API.custom_audio_adapter import CustomFFMPEGProcessAudioAdapter
import os

def separate_tracks(wav_file_path, output_directory):
    # Initialize Spleeter with the 4stems model
    separator = Separator('spleeter:4stems')

    # Initialize the custom audio adapter
    audio_adapter = CustomFFMPEGProcessAudioAdapter()

    # Separate the song
    separator.separate_to_file(wav_file_path, output_directory, audio_adapter=audio_adapter)
    print("Separation done. Check the output directory for the separated tracks.")

def extract_filename(file_path: str) -> str:
    """
    Extrae el nombre base del archivo sin la extensión.
    Args:
        file_path (str): La ruta del archivo, por ejemplo, 'track3.wav'.
    Returns:
        str: El nombre base del archivo, por ejemplo, 'track3'.
    """
    # Obtener el nombre del archivo sin la ruta
    base_name = os.path.basename(file_path)

    # Dividir el nombre del archivo en nombre y extensión
    name, _ = os.path.splitext(base_name)

    return name
