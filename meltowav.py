import matplotlib.pyplot as plt
import librosa
from IPython.display import Audio
import IPython
import scipy
import time
import pygame
import numpy as np
filename = 'spectre-copyrighted-ncs-release.mp3'
filename = 'smoke_bomb.wav'
y, sr = librosa.load(filename)
spec = librosa.feature.melspectrogram(y=y,sr=sr,n_fft=2048, hop_length=512,win_length=None, window='hann', center=True, 
pad_mode='reflect', 
power=2.0,
n_mels=128)

# step3 converting mel-spectrogrma back to wav file
res = librosa.feature.inverse.mel_to_audio(spec, 
                                           sr=sr, 
                                           n_fft=2048, 
                                           hop_length=512, 
                                           win_length=None, 
                                           window='hann', 
                                           center=True, 
                                           pad_mode='reflect', 
                                           power=2.0, 
                                           n_iter=32)
Audio(data=res, rate=sr)