import pyaudio
from beans_frontend import *
import wave
import whisper
from convo_processing import get_response
import requests
from KEYS import elabs_api, voice_api
import pygame
import time
import sys
import spotify_controller
import subprocess
import colorama
import threading
from pynput import keyboard
pygame.init() 

# os.environ["FFMPEG_BINARY"] = r"C:\ffmpeg\bin\ffmpeg.exe"
api_num = 0

class AudioRecorder:
    def __init__(self):
        self.recording = False
        self.frames = []
        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.frames = []
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=2,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024)
            print("Recording started...")
            threading.Thread(target=self._record).start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            print("Recording stopped.")
            self.stream.stop_stream()
            self.stream.close()
            self.save_recording()

    def _record(self):
        while self.recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def save_recording(self):
        wf = wave.open("recording.wav", 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        global model
        convo = model.transcribe("recording.wav", verbose=True, language='en', fp16=False)['text'].lower()
        response = get_response(convo) 
        with open('beans_log','a') as f:
            try:
                f.write(f'Response: {response}')
            except UnicodeEncodeError as uee:
                f.write(f'Error: {uee}\n')
        speak(response) 

recorder = AudioRecorder()

def on_press(key):
    if key == keyboard.Key.ctrl_l or key == keyboard.KeyCode.from_char('b'):
        recorder.start_recording()

def on_release(key):
    if key == keyboard.Key.ctrl_l or key == keyboard.KeyCode.from_char('b'):
        recorder.stop_recording()

def start_beans():
    """
    Starts beans
    """
    global model
    model = whisper.load_model("tiny")
    # Set up the listener
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        print("Press and hold 'Ctrl' or 'b' to start recording, release to stop.")
        listener.join()

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
            print('' + colorama.Fore.MAGENTA + response + colorama.Fore.RESET)

        # Playing audio
        words = pygame.mixer.Sound('output.mp3')
        if spotify_controller.sp is not None:
            spotify_controller.change_volume('down')
        # beans_frontend.window.switch_image()
        words.play()
        # beans_frontend.window.switch_image()
        time.sleep(words.get_length())
        if spotify_controller.sp is not None:
            spotify_controller.change_volume('up')
    except IndexError:
        sys.exit()
    except pygame.error:
        print("No more tokens. Switching API...")
        api_num += 1
        speak(response, first_try=False)
