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

pygame.init() 
os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\bin\ffmpeg.exe"
api_num = 0

def record_audio(duration=5, rate=44100, chunk=1024, channels=2, format=pyaudio.paInt16):
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    print(colorama.Style.DIM)
    for i in tqdm(range(0, int(rate / chunk * duration)), desc='Beans is listening'):
        data = stream.read(chunk)
        frames.append(data)
    print(colorama.Style.RESET_ALL)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open("recording.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def main_audio_loop():
    model = whisper.load_model("small")

    while True:    
        subprocess.run('cls', shell=True)
        print(birb)
        record_audio()
        print(colorama.Style.DIM)
        convo = model.transcribe("recording.wav", verbose=True, language='en', fp16=False)['text'].lower()
        print(colorama.Style.RESET_ALL)

        print(colorama.Style.DIM + convo + colorama.Style.RESET_ALL)
        if 'beans' in convo or 'beams' in convo or "bean's" in convo:
            response = get_response(convo) 
            speak(response) 

def speak(response, first_try=True):
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
            print('                     ' + colorama.Fore.MAGENTA + response + colorama.Fore.RESET)

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
