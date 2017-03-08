import os

# set the librosa cache prior to importing librosa
os.environ['LIBROSA_CACHE_DIR'] = '/mnt/ramdisk/librosa_cache'
os.environ['LIBROSA_CACHE_LEVEL'] = '50'


import pyaudio
import numpy as np
import time
# import librosa
# import librosa.display

from os import sys, path
sys.path.append("/home/pi/py/")
# import rpio_magnet
import gpio


pa = pyaudio.PyAudio()
frame_rate=44100
ontime = 0.01 # wie lange der magnet an ist

print("Frames per second:", frame_rate)

def callback(in_data, frame_count, time_info, flag):
    # print(time.time())

    audio_data = np.fromstring(in_data, dtype=np.float32)
    # audio_data has a float for the amplitude of each sound sample

    # Instead of printing, process here the audio chunk 'audio_data' with libROSA
    # y_harmonic, y_percussive = librosa.effects.hpss(audio_data)
    # y_percussive = librosa.effects.percussive(audio_data, margin=3.0)
    # tempo, beats=librosa.beat.beat_track(audio_data ,frame_rate)
    # print(audio_data)
    # print(len(audio_data))
    # print (beats)
    # frame_count is always 1024
    # time_info is not so interesting
    # flag is 0
    # print(frame_count)
    # print(beats)

    # last = 0
    # for b in beats:
    #   # print(b)
    #   beattimestamp = librosa.core.frames_to_time(b,frame_rate)
    #   time.sleep(beattimestamp-last)
    #   last = beattimestamp+ontime
    #   print("Time",beattimestamp)
    #   print("Magnet ein")
    #   time.sleep(ontime)
    #   print("Magnet ausschalten")

    # here we try to program our own peak detect. If we pass a threshold, we switch on the magnets
    threshold = 0.7
    for a in audio_data:
      a = abs(a)
      if a > threshold:
        sample = int(a * 100)
        gpio.mag_st(0, sample)
        gpio.mag_st(1, sample)
        gpio.mag_st(2, sample)
        gpio.mag_st(3, sample)
        print("Magnet ein")

        time.sleep(ontime)

        gpio.mag_st(0, 0)
        gpio.mag_st(1, 0)
        gpio.mag_st(2, 0)
        gpio.mag_st(3, 0)
        print("Magnet ausschalten")
        print(" ")

    return None, pyaudio.paContinue


# main program:
stream = pa.open(format=pyaudio.paFloat32,
                 channels=1,
                 rate=frame_rate,
                 # frames_per_buffer=int(frame_rate/2.5),
                 output=False,
                 input=True,
                 stream_callback=callback)

# rpio_magnet.setup()
gpio.setup()

stream.start_stream()
while stream.is_active():
    time.sleep(0.25)
stream.close()
pa.terminate()

librosa.cache.clear()

