from spleeter.separator import Separator
from custom_audio_adapter import CustomFFMPEGProcessAudioAdapter
import os

# Initialize Spleeter with the 4stems model
separator = Separator('spleeter:4stems')

# Path to the input song
input_song_path = 'frontend/uploaded_files/track3.wav'  # Replace with your song file path

# Path to the directory where you want to save the separated tracks
output_directory = 'frontend/separated_files'

# Initialize the custom audio adapter
audio_adapter = CustomFFMPEGProcessAudioAdapter()

# Separate the song
separator.separate_to_file(input_song_path, output_directory, audio_adapter=audio_adapter)

print("Separation done. Check the output directory for the separated tracks.")
