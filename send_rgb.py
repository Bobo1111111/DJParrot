import matplotlib.pyplot as plt
import librosa
from IPython.display import Audio
import time
import numpy as np
import serial

def strength_fre(y,sr,fmax,fmin):
    return librosa.onset.onset_strength(y=y,sr=sr,fmax=fmax,fmin=fmin)


COM_PORT = 'COM4'    # 指定通訊埠名稱
BAUD_RATES = 9600    # 設定傳輸速率
# ser = serial.Serial(COM_PORT, BAUD_RATES)   # 初始化序列通訊埠

def norm(x):
    return (x-np.min(x))/(np.max(x)-np.min(x))
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

filename = 'res/spectre-copyrighted-ncs-release.mp3'
y, sr = librosa.load(filename)
low = np.array(strength_fre(y,sr,1000,0))
mid = np.array(strength_fre(y,sr,2000,1000))
high = np.array(strength_fre(y,sr,3000,2000))
low = norm(low)
mid = norm(mid)
high = norm(high)

length = len(low)
print(length)
frame = range(0,length)
frame_times = librosa.frames_to_time(frame, sr=sr)
for i in range(0,length):
    low[i] = low[i] if low[i] >50/255 else 0
    mid[i] = mid[i] if mid[i] >50/255 else 0
    high[i] = high[i] if high[i] >50/255 else 0
low = moving_average(low,30)
r = np.intc(low *255)

g = np.intc(mid *255)
b = np.intc(high *255)
# plt.scatter(frame_times[350:450],r[350:450])
plt.plot(low[100:300])
plt.show()
print(frame_times[0:20])

# RGB字串
word = ''
for i in range(0,len(r)):
    word+=str(r[i])
    word+=str(g[i])
    word+=str(b[i])

# start = time.time() #起始時間
# '''
# # while i < len(frame_times):
#     # if (time.time()-start) > frame_times[i]:

# # while True:

#         # send = (str(r[i]).zfill(3)+str(g[i]).zfill(3)+str(b[i]).zfill(3))
#         # send = bytes('120120000')
#         # print(send)
#         # i+=1
#         # time.sleep(1)
#         # print("half cycle")
        
#         # while ser.in_waiting:
#         #     feedback = ser.readline().decode()  # 接收回應訊息並解碼
#         #     print(f'{len(feedback)},{feedback}')
#         #     ser.reset_input_buffer()
# # time.sleep(1)        
# # ser.write(b'101010')
# '''
# time.sleep(1)
# ser.write(b's')
# ser.write(b'0')
# ser.write(bytes(word,'utf-8'))
# ser.write(b'')
# ser.write(b'')
# # 接收指令
# while True:
#     while ser.in_waiting:
#         mcu_feedback = ser.readline().decode()
#         print(mcu_feedback)

