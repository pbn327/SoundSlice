from spleeter.separator import Separator
from custom_audio_adapter import CustomFFMPEGProcessAudioAdapter
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

    """
    # Obtener el nombre del archivo sin la ruta
    base_name = os.path.basename(file_path)

    # Dividir el nombre del archivo en nombre y extensión
    name, _ = os.path.splitext(base_name)

    return name

if __name__=='__main__':
    wavfile_path='/home/luis/code/pbn327/SoundSlice/frontend/uploaded_files/track4.wav'
    output_directory='/home/luis/code/pbn327/SoundSlice/frontend/separated_files'
    separate_tracks(wavfile_path,output_directory)
