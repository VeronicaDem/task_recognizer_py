# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import wave

import numpy as np
from stt import Model
import pyaudio
from pydub import AudioSegment
from io import BytesIO

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 10
modelPath = "C:\\Users\\Nica\\.local\\share\\coqui\\models\\Russian STT v0.1.0\\model.tflite"
def main():
    fileName = record()
    recognize(fileName)

def recognize(filePath):
    ds = Model(modelPath)
    output_audio = BytesIO()
    raw_audio = AudioSegment.from_wav(filePath)
    raw_audio.set_frame_rate(16000).set_channels(
        1).export(output_audio, "wav", codec="pcm_s16le")
    output_audio.seek(0)
    fin = wave.open(output_audio, 'rb')
    audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)

    fin.close()
    print(ds.stt(audio))

def record():
    fileName = "hello1.wav"
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(fileName, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    return fileName
main()
