import os

import pyaudio
import numpy as np
import time

from os import sys, path
sys.path.append("/home/pi/py/")
import pigpio_magnet as magnet

pa = pyaudio.PyAudio()
frame_rate = 44100
block_size = 100
ringlen = 300
threshold = 2000



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

def callback(in_data, frame_count, time_info, flag):
    # print(time.time())
    # print (time_info)
    # audio_data has a signed int16 for the amplitude of each sound sample
    # because in_data is just a string of bytes, we have to convert the data here:
    audio_data = np.fromstring(in_data, dtype=np.int16)

    # here we try to program our own peak detect. If we pass a threshold, we switch on the magnets
    left = audio_data[0::2]
    right = audio_data[1::2]
    
    # print (len(left),len(right))

    # get bass by averaging over the sample size
    a = np.average(left)
    b = np.average(right)
    
    #print (a, b)

    a = 3 * abs(a)
    b = 3 * abs(b)    
   
    # get amplitude overall by first absolute, then averaging over the sample size
    c = np.average(abs(left))
    d = np.average(abs(right))
    
    if a > threshold:
        sampleleft = int(a * 5 * 100/32767)
    else:
        sampleleft = 0

    ringbufferleft.extend(np.array([sampleleft]))
    sampleleft = ringbufferleft.get()[0]
    magnet.mag_st(1, sampleleft)
   
    sampleleft = int(c * 5 * 100/32767 )
    
    ringbufferleft_ampl.extend(np.array([sampleleft]))
    sampleleft = ringbufferleft_ampl.get()[0]
    magnet.mag_st(0, sampleleft)
    
    if b > threshold:
        sampleright = int(b * 5 * 100/32767)
    else:
        sampleright = 0
        
    ringbufferright.extend(np.array([sampleright])) #write
    sampleright = ringbufferright.get()[0] #read
    magnet.mag_st(2, sampleright)
    
    sampleright = int(d * 5 * 100/32767)
        
    ringbufferright_ampl.extend(np.array([sampleright])) #write
    sampleright = ringbufferright_ampl.get()[0] #read
    magnet.mag_st(3, sampleright)
    #print ("   %05d\r" % sample, end="", flush=True)
    
    magnet.start_dc()

    return None, pyaudio.paContinue
 






# haupt programm:
ringbufferleft = RingBuffer(ringlen)
ringbufferleft_ampl = RingBuffer(ringlen)
ringbufferright = RingBuffer(ringlen)
ringbufferright_ampl = RingBuffer(ringlen)

print("Frames per second:", frame_rate)

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

    print("============ started ==========\n")

    while stream.is_active():
        time.sleep(0.25)

finally:
    stream.stop_stream()
    stream.close()
    pa.terminate()
    magnet.clear()



