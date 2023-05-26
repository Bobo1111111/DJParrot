import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import librosa
import numpy as np
'''
做一個library
能強度畫圖
'''

def beat_strength_graph(y,sr,beat_frames,onset_data,type = 'time',step = 30):
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    onset = []
    onset_time = []
    if type == 'time':
        for i in range (0,len(beat_frames)):
            onset.append(onset_data[beat_frames[i]])
            onset_time.append(beat_times[i])
        plt.figure(figsize=(20, 6))
        # librosa.display.waveshow(np.array([beat_times,onset]), x_axis='time')
        plt.axes().xaxis.set_major_locator(MultipleLocator(step))
        plt.scatter(beat_times,onset)
        plt.plot(beat_times,onset)
        plt.show()
    else:
        for i in range (0,len(beat_frames)):
            onset.append(onset_data[beat_frames[i]])
        plt.figure(figsize=(20, 6))
        plt.scatter(beat_frames,onset)
        plt.plot(beat_frames,onset)
        plt.show()

def fre_graph_1(y,sr,fmax=8192,fmin=0):
    D = np.abs(librosa.stft(y))
    times = librosa.times_like(D)
    fig, ax = plt.subplots(nrows = 2, sharex = True, figsize=(20, 6))
    librosa.display.specshow(librosa.amplitude_to_db(D, ref = np.max), y_axis='log',x_axis='time', ax=ax[0])
    ax[0].set(title='Power spectrogram')
    ax[0].label_outer()
    onset_lowf = librosa.onset.onset_strength(y=y, sr=sr, fmax = fmax, fmin = fmin)
    ax[1].plot(times,onset_lowf/onset_lowf.max(),label = f'{fmax}Hz')
    ax[1].legend()
    plt.show()

def strength_fre(y,sr,fmax,fmin):
    return librosa.onset.onset_strength(y=y,sr=sr,fmax=fmax,fmin=fmin)


if __name__ == '__main__':
    
    filename = 'spectre-copyrighted-ncs-release.mp3'
    y, sr = librosa.load(filename)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    # fre_graph_1(y,sr)
    i=0
    onset_data = strength_fre(y,sr,2**(i+1)*64,2**i*64)
    beat_strength_graph(y,sr,beat_frames,onset_data,type = 'time',step = 30)
    


