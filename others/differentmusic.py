import matplotlib.pyplot as plt
import librosa
from IPython.display import Audio
import IPython
import scipy
import time
import pygame
import numpy as np
filename = librosa.example('brahms')
y, sr = librosa.load(filename)
librosa.display.waveshow(y,sr=sr)
plt.show()
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
plt.plot(onset_env)
plt.show()