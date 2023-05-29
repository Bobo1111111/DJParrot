import matplotlib.pyplot as plt
import librosa
from IPython.display import Audio
import IPython
import scipy
import time
import pygame
import numpy as np
import urllib.request
from oo import *

filename = 'spectre-copyrighted-ncs-release.mp3'
y, sr = librosa.load(filename)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print(60/tempo)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
first_beat_time = beat_times[0]

onset_data = strength_fre(y,sr,1000,0)

all = []
low = []
low_stg = []
high = []
high_stg  = []
threshold = 6
if onset_data[beat_frames[0]] >= threshold:
    high.append(beat_frames[0])
    high_stg.append(onset_data[beat_frames[0]])
    all.append('h')
else:
    low.append(beat_frames[0])
    low_stg.append(onset_data[beat_frames[0]])
    all.append('l')

for i in range(1,len(beat_frames)):
    if onset_data[beat_frames[i]] >= threshold or (onset_data[beat_frames[i]] - onset_data[beat_frames[i-1]] >1.5 and onset_data[beat_frames[i]]>3):
        high.append(beat_frames[i])
        high_stg.append(onset_data[beat_frames[i]])
        all.append('h')

    else:
        low.append(beat_frames[i])
        low_stg.append(onset_data[beat_frames[i]])
        all.append('l')

low_time = librosa.frames_to_time(low, sr=sr)
high_time = librosa.frames_to_time(high, sr=sr)

beat_times = librosa.frames_to_time(beat_frames, sr=sr)
onset = []
onset_time = []
for i in range (0,len(beat_frames)):
    onset.append(onset_data[beat_frames[i]])
    onset_time.append(beat_times[i])

pygame.mixer.init()
low_sound = pygame.mixer.Sound("drum.wav")
low_sound.set_volume(0.6)
high_sound = pygame.mixer.Sound("high.wav")
high_sound.set_volume(1)
pygame.mixer.music.load(filename)
pygame.mixer.music.play()
start = time.time() #起始時間

i = 0
j = 0
while i < len(low_time) and j < len(high_time):
    if (time.time()-start) > low_time[i]-0.1:
        pygame.mixer.Sound.play(low_sound)
        # urllib.2
        # request.urlopen(r'http://192.168.130.253/H')
        # time.sleep(0.05)
        # urllib.request.urlopen(r'http://192.168.130.253/L')
        i+=1
    if (time.time()-start) > high_time[j]-0.1:
        pygame.mixer.Sound.play(high_sound)
        j+=1