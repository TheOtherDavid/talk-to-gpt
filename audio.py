from collections import deque
import sounddevice as sd
import numpy as np
import pyaudio
import struct
import io
from io import BytesIO
import os
import time
import requests
import wave
import gtts
from pydub import AudioSegment
from playsound import playsound

def record_audio_for_duration(duration, filename):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    seconds = duration

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
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    return AudioSegment.from_file(filename, format="wav")

def record_audio_until_keystroke(filename):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    frames = []  # Initialize array to store frames

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording. Press any key to stop.')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    # Store data in chunks until the user presses a key
    while True:
        data = stream.read(chunk)
        frames.append(data)

        # Check if a key has been pressed
        if input_check():
            break

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()

    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return AudioSegment.from_file(filename, format="wav")

# Helper function to check if a key has been pressed
def input_check():
    import msvcrt
    return msvcrt.kbhit()

def save_audio(buffer):
    audio_data = buffer.getvalue()
    audio = AudioSegment.from_raw(io.BytesIO(audio_data),
                                  format="raw",
                                  sample_width=2,
                                  channels=1,
                                  frame_rate=44100)

    audio.export("output.mp3", format="mp3")
    print("Saved audio to output.mp3")

def wave_header(sample_rate, channels, dtype):
    bits_per_sample = np.dtype(dtype).itemsize * 8
    byte_rate = sample_rate * channels * bits_per_sample // 8
    block_align = channels * bits_per_sample // 8

    header = b'RIFF'
    header += struct.pack('<I', 36 + 2 * sample_rate)
    header += b'WAVEfmt '
    header += struct.pack('<I', 16)  # fmt chunk size
    header += struct.pack('<H', 1)  # format tag (PCM)
    header += struct.pack('<H', channels)
    header += struct.pack('<I', sample_rate)
    header += struct.pack('<I', byte_rate)
    header += struct.pack('<H', block_align)
    header += struct.pack('<H', bits_per_sample)
    header += b'data'
    header += struct.pack('<I', 2 * sample_rate)  # data chunk size

    return header

def convert_text_to_audio(text):
    tts = gtts.gTTS(text, lang="en")
    tts.save("response.mp3")
    # Load the audio file
    sound = AudioSegment.from_mp3("response.mp3")

    # Speed up the playback speed by 1.25 times
    #sound = sound.speedup(playback_speed=1)

    # Play the modified audio file
    sound.export("response.mp3", format="mp3")
    play_audio("response.mp3")

def play_audio(filename):
    # Load the audio file with pydub
    sound = AudioSegment.from_file(filename, format="mp3")

    # Speed up the playback speed with pydub
    playback_speed=1.25
    sound = sound.speedup(playback_speed)

    # Export the modified audio to a wave file
    sound.export("modified.wav", format="wav")

    # Open the wave file with wave
    with wave.open("modified.wav", "rb") as audio_file:
        audio_data = audio_file.readframes(audio_file.getnframes())

    # Play the audio data with pyaudio
    audio_player = pyaudio.PyAudio()
    stream = audio_player.open(format=audio_player.get_format_from_width(audio_file.getsampwidth()),
                               channels=audio_file.getnchannels(),
                               rate=audio_file.getframerate(),
                               output=True)
    stream.write(audio_data)

    # Close the audio stream and the PyAudio object
    stream.stop_stream()
    stream.close()
    audio_player.terminate()

if __name__ == "__main__":
    record_audio_for_duration(5,"test.wav")
    convert_text_to_audio("I have extra wood")
