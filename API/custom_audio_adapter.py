import subprocess
import numpy as np
import os
from spleeter.audio.adapter import AudioAdapter

class CustomFFMPEGProcessAudioAdapter(AudioAdapter):
    def load(self, path, offset=0, duration=0, sample_rate=44100, dtype=np.float32):
        command = [
            'ffmpeg',
            '-y',  # Overwrite output files without asking
            '-i', path,
            '-ss', str(offset),
            '-t', str(duration) if duration > 0 else 'inf',
            '-ar', str(sample_rate),
            '-ac', '2',  # Always force stereo output
            '-f', 'f32le',  # Output format
            'pipe:1'  # Output to stdout
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg process failed with error: {stderr.decode()}")
        audio_data = np.frombuffer(stdout, dtype=dtype)
        if len(audio_data) % 2 != 0:
            audio_data = audio_data[:-1]
        print(f"Loaded audio data with shape: {audio_data.shape}")
        return audio_data.reshape(-1, 2), sample_rate

    def save(self, path, data, sample_rate=44100, codec=None, bitrate=None):
        temp_path = path + '.wav'
        self._save_wav(temp_path, data, sample_rate)
        if not os.path.exists(temp_path):
            print(f"Temporary WAV file was not created: {temp_path}")
            return

        command = [
            'ffmpeg',
            '-y',
            '-i', temp_path,
            '-vn',  # No video
            '-ar', str(sample_rate),
            path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"FFmpeg failed to convert file: {result.stderr.decode()}")
        else:
            print(f"Saved file to: {path}")

        os.remove(temp_path)

    def _save_wav(self, path, data, sample_rate):
        command = [
            'ffmpeg',
            '-y',
            '-f', 'f32le',
            '-ar', str(sample_rate),
            '-ac', '2',
            '-i', 'pipe:0',
            path
        ]
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=data.astype(np.float32).tobytes())
        if process.returncode != 0:
            print(f"FFmpeg failed to save WAV file: {stderr.decode()}")
        else:
            print(f"WAV file saved to: {path}")
