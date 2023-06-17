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
import copy
import serial

# some dunction for music analysis
def norm(x):
    return (x-np.min(x))/(np.max(x)-np.min(x))

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def strength_fre(y,sr,fmax,fmin):
    return librosa.onset.onset_strength(y=y,sr=sr,fmax=fmax,fmin=fmin)

# Serial init

COM_PORT_LED = 'COM4'
COM_PORT_MOTOR = 'COM5'
BAUD_RATES = 9600

ser_LED = serial.Serial(COM_PORT_LED, BAUD_RATES)
ser_MOTOR = serial.Serial(COM_PORT_MOTOR, BAUD_RATES)

# get data from mp3 file
filename = 'res/spectre-copyrighted-ncs-release.mp3'
y, sr = librosa.load(filename)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# beat
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# beat onset(same as red)
onset_data = strength_fre(y,sr,1000,0)

# LED onset(different freq)
low = np.array(strength_fre(y,sr,1000,0))
mid = np.array(strength_fre(y,sr,2000,1000))
high = np.array(strength_fre(y,sr,3000,2000))

# normalize LED onset
low = norm(low)
mid = norm(mid)
high = norm(high)

# get the length of the LED data
length = len(low)

# know the exact time of each frame for LED
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

# save data for motor control
r_copy = r[:]

# 將LED (0,0,0) 給去掉，avoid no light
i = 0
while i < len(frame_times):
    if r[i]==0 and g[i]==0 and b[i]==0:
        r = np.delete(r,[i])
        g = np.delete(g,[i])
        b = np.delete(b,[i])
        frame_times = np.delete(frame_times,[i])
    else:
        i+=1

length_LED = len(frame_times)
to_send = []
for i in range(0,length_LED):
    # RGB字串
    a = "s"+str(r[i]).zfill(3)+str(g[i]).zfill(3)+str(b[i]).zfill(3)
    to_send.append(a)

# time: frame_times; data: to_send: 


# motor

# each time of the beat
beat_times = librosa.frames_to_time(beat_frames, sr=sr)
length_beat = len(beat_times)

# 想計算一拍間有幾個重拍(the old r)
strong_beat_number = []
for i in range(0,len(beat_frames)-1):
    strong_beat_number.append(0)
    for j in r_copy[beat_frames[i]:beat_frames[i+1]]:
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

# time: beat_times; send: all


full_send_time = []
full_send_action = []

'''
h: 重拍
l: 輕拍
c: 碎拍
'''


# play music
pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play()
print("start")

# record current time
start_time = time.time()

index_LED = 0
index_motor = 0
while index_motor < len(beat_times):

    if time.time() - start_time > beat_times[index_motor]:
        ser_MOTOR.write(bytes(all[index_motor],'utf-8'))
        index_motor += 1
    
    if time.time() - start_time > frame_times[index_LED]:
        ser_LED.write(bytes(to_send[index_LED],'utf-8'))
        index_LED += 1
