import pyaudio
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

pygame.init() 
api_num = 0

def record_audio(duration=5, rate=44100, chunk=1024, channels=2, format=pyaudio.paInt16):
    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    print("Recoding audio...")

    print(birb)

    for i in tqdm(range(0, int(rate / chunk * duration))):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Saving audio...")

    wf = wave.open("recording.wav", 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Recording complete.\n")


def main_audio_loop():
    model = whisper.load_model("medium")

    while True:    
        record_audio()
        convo = model.transcribe("recording.wav", verbose=False, language='en', fp16=False)['text'].lower()
        print(convo)
        if 'beans' in convo or 'beams' in convo or "bean's" in convo:
            print("Name heard!")
            response = get_response(convo) 
            speak(response) 

def speak(response, first_try=True):
    global api_num
    if first_try:
        print("Speaking...")
    CHUNK_SIZE = 1024
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_api[api_num]}"
        # print(url)
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
        # print(data)
        output = requests.post(url, json=data, headers=headers)
        with open('output.mp3', 'wb') as f:
            for chunk in output.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)
        if first_try:
            print(birb_talking)

        # Playing audio
        words = pygame.mixer.Sound('output.mp3')
        if spotify_controller.sp is not None:
            spotify_controller.change_volume('down')
        words.play()
        time.sleep(words.get_length())
        if spotify_controller.sp is not None:
            spotify_controller.change_volume('up')


        print("Speaking complete.")
    except IndexError:
        sys.exit()
    except pygame.error:
        print("No more tokens. Switching API...")
        api_num += 1
        speak(response, first_try=False)
