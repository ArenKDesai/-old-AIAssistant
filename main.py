# import pygame
from audio import main_audio_loop, pedal_loop
import colorama
import sys
colorama.init()

if __name__ == "__main__":
    for arg in sys.argv:
        if '--pedal' in arg:
            pedal_loop()
    else:
        main_audio_loop()