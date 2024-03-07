import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import pygame
import os
import pyaudio
import wave
import glob
from time import sleep
import librosa

def play_audio(file_path):
    """
    Play an audio file wav or mp3
    """

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


def test():
    """
    Test if the recording stuff works
    """

    # Set the microphone settings
    sample_rate = 44100
    channels = 2

    # Set the duration for each recording block (in seconds)
    block_duration = 5
    
    input_devices = sd.query_devices(kind='input')
    print(input_devices)
    recording = sd.rec(int(sample_rate * block_duration), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()
    print(f'Recording audio: {recording}')
    myrecording = sd.playrec(recording, sample_rate, channels=channels)



def record_audio(output_file, duration=5, sample_rate=44100, channels=1, format=pyaudio.paInt16):
    """
    Record audio and save it to a WAV file.

    Parameters:
    - output_file: The path to save the recorded audio as a WAV file.
    - duration: Recording duration in seconds.
    - sample_rate: Sampling rate of the audio (default is 44100 Hz).
    - channels: Number of audio channels (1 for mono, 2 for stereo).
    - format: Audio sample format (default is 16-bit PCM).

    Returns:
    None
    """
    p = pyaudio.PyAudio()

    try:
        stream = p.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=1024)

        print("Recording...")

        frames = []
        for i in range(0, int(sample_rate / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)

        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

        print(f"Audio saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        p.terminate()


def get_random_audio_file():
    """
    Get a random drachenlord audio
    """

    files = glob.glob('data/d*.*')
    n_f = len(files)
    i_f = np.random.randint(0, n_f)

    return files[i_f]


def main(threshold=1, duration=1):
    """
    Execute stuff
    """

    # Set the microphone threshold (adjust as needed)
    threshold = int(threshold * 100)
    #print(f'Threshold value: {threshold}')

    # Set the microphone settings
    sample_rate = 44100
    channels = 2

    # Set the duration for each recording block (in seconds)
    block_duration = duration
    #print(f'Duration value: {duration}')
    
    input_devices = sd.query_devices(kind='input')

    # Set the path to your MP3 file
    audio_file_path = get_random_audio_file() #'data/drachen1.mp3'
    print(f'Audio file: {audio_file_path}')
    
    # Record microphone input
    recording = sd.rec(int(sample_rate * block_duration), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()
    print(f'Mean: {np.abs(recording).mean()} Threshold: {threshold}')

    # Check if the average amplitude is above the threshold
    if np.abs(recording).mean() > threshold:

        print("Sound detected!")
        sleep(1)
        # Play the chosen MP3 file
        play_audio(audio_file_path)
        audio_len = librosa.get_duration(filename=audio_file_path)
        print(f"Audio len: {audio_len}")
        sleep(audio_len)


def main_loop(threshold=1, duration=1, execute=True):
    """
    Execute stuff
    """

    # Set the microphone threshold (adjust as needed)
    threshold = int(threshold * 100)
    #print(f'Threshold value: {threshold}')

    # Set the microphone settings
    sample_rate = 44100
    channels = 2

    # Set the duration for each recording block (in seconds)
    block_duration = duration
    #print(f'Duration value: {duration}')
    
    input_devices = sd.query_devices(kind='input')

    while execute:
        # Set the path to your MP3 file
        audio_file_path = get_random_audio_file() #'data/drachen1.mp3'
        print(f'Audio file: {audio_file_path}')
        
        # Record microphone input
        recording = sd.rec(int(sample_rate * block_duration), samplerate=sample_rate, channels=channels, dtype='int16')
        sd.wait()
        print(f'Mean: {np.abs(recording).mean()} Threshold: {threshold}')

        # Check if the average amplitude is above the threshold
        if np.abs(recording).mean() > threshold:

            print("Sound detected!")
            sleep(1)
            # Play the chosen MP3 file
            play_audio(audio_file_path)
            audio_len = librosa.get_duration(filename=audio_file_path)
            print(f"Audio len: {audio_len}")
            sleep(audio_len)


if __name__ == "__main__":
    """
    Go!
    """

    #test()
    #record_audio('tmp.wav')
    main(10)
    #play()
    #get_random_audio_file()
