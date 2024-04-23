import pyaudio
import wave
import threading
import whisper
from convo_processing import process_convo

def record_audio(model, duration=3, rate=44100, chunk=1024, channels=2, format=pyaudio.paInt16):
    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    for i in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

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
    model = whisper.load_model("medium")

    while True:
        record_audio(model)
        convo = whisper.listen("recording.wav").lower()
        if 'pluto' in convo:
            while convo:
                tag = process_convo(convo)
                response = "" # TODO: get gpt's response
                # TODO: 
