import matplotlib.pyplot as plt
import librosa
from IPython.display import Audio
import time
import numpy as np
import serial
import pygame

# some dunction for music analysis
def norm(x):
    return (x-np.min(x))/(np.max(x)-np.min(x))

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def strength_fre(y,sr,fmax,fmin):
    return librosa.onset.onset_strength(y=y,sr=sr,fmax=fmax,fmin=fmin)


COM_PORT = 'COM3'    # 指定通訊埠名稱
BAUD_RATES = 9600    # 設定傳輸速率
ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠


# get data from mp3 file
filename = 'res/spectre-copyrighted-ncs-release.mp3'
y, sr = librosa.load(filename)
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

# 可能要考慮移動平均？
# low = moving_average(low,30)

# from 0-1 to 0-255
r = np.intc(low *255)
g = np.intc(mid *255)
b = np.intc(high *255)
# plt.scatter(frame_times[350:450],r[350:450])

# #show how it looks
# plt.plot(frame_times[0:600],high[:600])
# plt.show()

# 將(0,0,0)給去掉
i = 0
while i < len(frame_times):
    if r[i]==0 and g[i]==0 and b[i]==0:
        r = np.delete(r,[i])
        g = np.delete(g,[i])
        b = np.delete(b,[i])
        frame_times = np.delete(frame_times,[i])
    else:
        i+=1

length = len(frame_times)
to_send = []
for i in range(0,length):
    # RGB字串
    a = "s"+str(r[i]).zfill(3)+str(g[i]).zfill(3)+str(b[i]).zfill(3)
    to_send.append(a)
print(frame_times)
print(to_send)

pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play()
print("start")
start_time = time.time()

index = 0
while True:
    if time.time() - start_time > frame_times[index]:
        ser.write(bytes(to_send[index],'utf-8'))
        index += 1
    if ser.in_waiting:
        feedback = ser.readline().decode()  # 接收回應訊息並解碼+
        print(f'{feedback}')

