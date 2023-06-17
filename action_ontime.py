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

filename = 'res/spectre-copyrighted-ncs-release.mp3'
y, sr = librosa.load(filename)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
# print(beat_frames)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
first_beat_time = beat_times[0]

onset_data = strength_fre(y,sr,1000,0)

# some dunction for music analysis
def norm(x):
    return (x-np.min(x))/(np.max(x)-np.min(x))
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

low = np.array(strength_fre(y,sr,1000,0))
mid = np.array(strength_fre(y,sr,2000,1000))
high = np.array(strength_fre(y,sr,3000,2000))

# normalize all data first
low = norm(low)
mid = norm(mid)
high = norm(high)

#  get the length of the data
length = len(low)

# know the exact time of each frame
frame = range(0,length)
frame_times = librosa.frames_to_time(frame, sr=sr)

# cut the light too low
for i in range(0,length):
    low[i] = low[i] if low[i] >50/255 else 0
    mid[i] = mid[i] if mid[i] >50/255 else 0
    high[i] = high[i] if high[i] >50/255 else 0

# from 0-1 to 0-255
r = np.intc(low *255)
g = np.intc(mid *255)
b = np.intc(high *255)

# 想計算一拍間有幾個重拍
strong_beat_number = []
for i in range(0,len(beat_frames)-1):
    strong_beat_number.append(0)
    for j in r[beat_frames[i]:beat_frames[i+1]]:
        if j > 0:
            strong_beat_number[i] += 1


# 存每個beat是大或小
all = []

threshold = 6
if onset_data[beat_frames[0]] >= threshold:
    all.append('h')
else:
    all.append('l')

for i in range(1,len(beat_frames)):
    if onset_data[beat_frames[i]] >= threshold or (onset_data[beat_frames[i]] - onset_data[beat_frames[i-1]] >1.5 and onset_data[beat_frames[i]]>3):
        all.append('h')
    else:
        all.append('l')

for i in range(0,len(all)-1):
    if strong_beat_number[i] >= 6:
        all[i] = 'c'
# print(all)
all_num = np.array(all)
all_num = all_num.reshape((-1,4))
print(all_num)
print(len(beat_times))
print(len(all))
print(all_num.shape)

'''
h: 重拍
l: 輕拍
c: 碎拍
'''

# each time of the beat
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
length_beat = len(beat_times)

pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play()
print("start")
start_time = time.time()
index = 0
while index < len(beat_times):
    if time.time() - start_time > beat_times[index]:
        print(all[index])
        index += 1
