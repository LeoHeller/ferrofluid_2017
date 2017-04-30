import os

# set the librosa cache prior to importing librosa
os.environ['LIBROSA_CACHE_DIR'] = '/mnt/ramdisk/librosa_cache'
os.environ['LIBROSA_CACHE_LEVEL'] = '50'


import pyaudio
import numpy as np
import time
#import librosa
#import librosa.display

from os import sys, path
sys.path.append("/home/pi/py/")
#import rpio_magnet
import pigpio_magnet as magnet

pa = pyaudio.PyAudio()
frame_rate = 44100
block_size = 100
ontime = 0.01 # wie lange der magnet an ist
ringlen = 300
threshold = 2000


print("Frames per second:", frame_rate)


class RingBuffer():
    "A 1D ring buffer using numpy arrays"
    def __init__(self, length):
        self.data = np.zeros(length, dtype='i')
        self.index = 0

    def extend(self, x):
        "adds array x to ring buffer"
        x_index = (self.index + np.arange(x.size)) % self.data.size
        self.data[x_index] = x
        self.index = x_index[-1] + 1

    def get(self):
        "Returns the first-in-first-out data in the ring buffer"
        idx = (self.index + np.arange(self.data.size)) %self.data.size
        return self.data[idx]

ringbufferleft = RingBuffer(ringlen)
ringbufferright = RingBuffer(ringlen)

def callback(in_data, frame_count, time_info, flag):
    # print(time.time())
    # print (time_info)
    audio_data = np.fromstring(in_data, dtype=np.int16)
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
    left = audio_data[0::2]
    right = audio_data[1::2]
    
    # print (len(left),len(right))

    a = np.average(left)
    b = np.average(right)
    
    #print (a, b)

    a = abs(a)
    b = abs(b)    
   
    if a > threshold:
        sampleleft = int(a * 100/32767 * 5)
        
    else:
        sampleleft = 0
    
    ringbufferleft.extend(np.array([sampleleft]))
    sampleleft = ringbufferleft.get()[0]
    magnet.mag_st(1, sampleleft)
    
    if b > threshold:
        sampleright = int(b * 100/32767 * 5)

    else:
        sampleright = 0
        
    ringbufferright.extend(np.array([sampleright])) #write
    sampleright = ringbufferright.get()[0] #read
    magnet.mag_st(2, sampleright)
    #print ("   %05d\r" % sample, end="", flush=True)
    
    magnet.start_dc()

    return None, pyaudio.paContinue
 
# haupt programm:

magnet.setup()

stream = pa.open(format=pyaudio.paInt16,
                 channels=2,
                 rate=frame_rate,
                 # frames_per_buffer=int(frame_rate/2.5),
                 frames_per_buffer = block_size,
                 output=False,
                 input=True,
                 stream_callback=callback)

try:    
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.25)

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    # librosa.cache.clear()
    magnet.clear()



