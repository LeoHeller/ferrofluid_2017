import librosa
import librosa.display
import IPython.display
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as ms
ms.use('seaborn-muted')

print ('a')
# Load the example track
y, sr = librosa.load('/home/pi/music/soft.wav', duration=20.0)
print ('b')
#y_h, y_p = librosa.effects.hpss(y)
tempo, beats=librosa.beat.beat_track(y,sr)

print (beats)
print ('c')



#librosa.output.write_wav('/tmp/my.wav',y_h,sr)
