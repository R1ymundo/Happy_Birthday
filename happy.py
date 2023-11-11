
import scipy.io.wavfile as wavfile
import numpy as np
import time
import os
from scipy import mean
from random import randint
import pygame

# Inicializar Pygame para reproducir audio
pygame.mixer.init()

# music wav file
FILE = "karaoke.wav"
rate, data = wavfile.read(FILE)
t_total = len(data[:, 0]) / rate
display_rate = 1500  # number of frames processed in one iteration
sample_size = 120
max_display = 90
data_length = len(data)  # total number of frames
_min = min([abs(x) for x in data[:, 0]])  # max amplitude in the wav
_max = max([abs(x) for x in data[:, 0]])  # min amplitude in the wav

# IMPORTANT: correction factor. Change this value to match the song with equalizer
correction = 0.645

# cake settings
cols = 80  # Default value, adjust as needed
display_char = "8"
cake_size = 50

# flame control
flame_flutter_rate = 50
FLAMES = [" . ", ".  ", "  ."]
current_flame = ""

os.system("cls")  # Clear the console

# Reproducir música
pygame.mixer.music.load(FILE)
pygame.mixer.music.play()

for _f in range(data_length // display_rate):

    # fluttering effect to candle flames
    if _f % flame_flutter_rate == 0:
        current_flame = (" " * (cols // 2 - cake_size // 2)) + ((" " + FLAMES[randint(0, 2)] + " ") * (cake_size // 5))
    print(current_flame)

    # candles
    print(" " * (cols // 2 - cake_size // 2) + ("  |  " * (cake_size // 5)))
    # cake top layer
    print(" " * (cols // 2 - cake_size // 2) + ("-" * cake_size))

    bucket = []
    mug = []
    # mug contains the current frame samples (absolute values) of given sample_size
    # average of mugs are put into bucket
    for value in data[:, 0][_f * display_rate + 1:(_f + 1) * display_rate]:
        mug.append(abs(value))
        if len(mug) == sample_size:
            bucket.append(mean(mug))
            mug = []
    bucket = [(float((x - _min) * max_display) / (_max - _min)) for x in bucket]

    # print the equalizer from the bucket
    for value in bucket:
        print(" " * (cols // 2 - cake_size // 2) + "| " + ("8" * (int(value) % (cake_size - 2))) + (
                " " * (cake_size - int(value) - 2)) + "|")

    # bottom crust of the cake
    print(" " * (cols // 2 - cake_size // 2) + ("-" * cake_size))

    # print happy birthday message
    print("				¡Happy Birthday Name!")

    # sleep to match with the audio
    time.sleep(((float)(display_rate * t_total) / data_length) * correction)

    # clear screen
    if _f != data_length // display_rate - 1:
        os.system("cls")
