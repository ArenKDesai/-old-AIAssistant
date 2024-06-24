import pyaudio
import os
import wave
import whisper
from convo_processing import get_response
import requests
from KEYS import elabs_api, voice_api
import pygame
import time
from tqdm import tqdm
from ascii_art import birb, birb_talking
import sys
import spotify_controller
import subprocess
import colorama
from pynput import keyboard
pygame.init() 

os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\bin\ffmpeg.exe"
api_num = 0

def record_audio(pyaudio_instance, pedal=False, duration=5, rate=44100, chunk=1024, channels=2, format=pyaudio.paInt16):
    """
    Allows for Beans to hear audio
    Parameters:
        pedal: bool, if true then it uses the pedal (b key) instead of duration
        duration: int, seconds that Beans listens before thinking
        rate: int, how quickly beans will process audio input
        chunks: int, how much data beans will hear at once
        channels: how many channels the audio devices has
        format: format of audio recording
    Return:
        Saves 'recording.wav' in cwd
    """
    stream = pyaudio_instance.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    # Dim the recoding so Beans stands out
    print(colorama.Style.DIM)
    if pedal:
        # Set up keyboard listener
        recording = False
        def on_press(key):
            nonlocal recording
            try:
                if key.char == 'b' and not recording:
                    recording = True
            except AttributeError:
                pass

        def on_release(key):
            nonlocal recording
            try:
                if key.char == 'b' and recording:
                    recording = False
                    return False  # Stop listener
            except AttributeError:
                pass

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        # Wait for 'b' key press to start recording
        print("Press the foot pedal (b key) to start recording...")
        while not recording:
            pass

        # Record until 'b' key is released
        with tqdm(desc='Beans is listening', unit=' chunks') as pbar:
            while recording:
                data = stream.read(chunk)
                frames.append(data)
                pbar.update(1)

        listener.stop()
    else:
        for i in tqdm(range(0, int(rate / chunk * duration)), desc='Beans is listening'):
            data = stream.read(chunk)
            frames.append(data)
    # Remove dim
    print(colorama.Style.RESET_ALL)

    stream.stop_stream()
    stream.close()
    # TODO: not closing pyaudio_instance

    wf = wave.open("recording.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio_instance.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def main_audio_loop(pyaudio_instance, model):
    """
    Function called during Beans brain loop that allows Beans to hear and speak
    """

    subprocess.run('cls', shell=True)
    print(birb)
    # Call function to record audio, default 5 seconds
    record_audio(pyaudio_instance=pyaudio_instance)
    print(colorama.Style.DIM)
    # STT from OpenAI Whisper
    convo = model.transcribe("recording.wav", verbose=True, language='en', fp16=False)['text'].lower()
    print(colorama.Style.RESET_ALL)

    if 'beans' in convo or 'beams' in convo or "bean's" in convo:
        # Process response with Beans GPT
        response = get_response(convo) 
        # Get Beans to speak the response
        speak(response) 

def pedal_loop(pyaudio_instance, model):
    """
    Function called during Beans brain loop that allows Beans to hear and speak
    This one is called if the pedal is active
    """

    subprocess.run('cls', shell=True)
    print(birb)
    record_audio(pedal=True,pyaudio_instance=pyaudio_instance)
    print(colorama.Style.DIM)
    convo = model.transcribe("recording.wav", verbose=True, language='en', fp16=False)['text'].lower()
    print(colorama.Style.RESET_ALL)

    print(colorama.Style.DIM + convo + colorama.Style.RESET_ALL)
    response = get_response(convo) 
    with open('beans_log','a') as f:
        try:
            f.write(f'Response: {response}')
        except UnicodeEncodeError as uee:
            f.write(f'Error: {uee}\n')
    speak(response) 

def speak(response:str, first_try=True):
    global api_num
    CHUNK_SIZE = 1024
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_api[api_num]}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": f"{elabs_api[api_num]}"
        }

        data = {
            "text": response,
            "model_id": "eleven_turbo_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        output = requests.post(url, json=data, headers=headers)
        with open('output.mp3', 'wb') as f:
            for chunk in output.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        if first_try:
            subprocess.run('cls', shell=True)
            print(birb_talking)
            print('             ' + colorama.Fore.MAGENTA + response + colorama.Fore.RESET)

        # Playing audio
        words = pygame.mixer.Sound('output.mp3')
        if spotify_controller.sp is not None:
            spotify_controller.change_volume('down')
        words.play()
        time.sleep(words.get_length())
        if spotify_controller.sp is not None:
            spotify_controller.change_volume('up')
    except IndexError:
        sys.exit()
    except pygame.error:
        print("No more tokens. Switching API...")
        api_num += 1
        speak(response, first_try=False)
