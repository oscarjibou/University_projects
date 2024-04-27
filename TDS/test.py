import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import scipy.signal as signal
import librosa

sys.path.append("/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS"
                )

from scipy.io import wavfile
from utils import split_signal_into_frames, cut_signal_frames, cut_signal_frames2

'''
- Extract the audio signal from the wav file and plot it
- normalize and convert the audio signal to mono
- trim the audio signal
- split the singnal and plot ir 
'''

frequency_audio, audio = wavfile.read("P4/nine.wav")

tiempo_señal = 1/frequency_audio * np.arange(len(audio))

audio = audio / np.max(np.abs(audio))

yt, index = librosa.effects.trim(
    audio, top_db=20, frame_length=2048, hop_length=512)

audio = audio[index[0]:index[1]] # convert to mono

audio_frames = split_signal_into_frames(audio, frequency_audio,0.32, 0)
audio_frames2 = cut_signal_frames(audio, frequency_audio, 0.32)
audio_frames3 = cut_signal_frames2(audio, frequency_audio, 0.32)

#which is the shape of audio_frames3
print(tiempo_señal.shape)
print(np.shape(audio_frames3))

new_time = np.arange(0, len(audio)/2, 1)

print(new_time.shape)
print(np.shape(audio_frames3))


# print(audio_frames)
# print(audio_frames2)
# print(audio_frames3)

#print(tiempo_señal)


#plot audio_frames3
# plt.figure(figsize=(10, 5))
# plt.plot(new_time, audio_frames3[0])
# plt.title(f"Frames of 32ms")
# plt.xlabel("Time [s]")
# plt.ylabel("Amplitude")
# plt.show()

# plt.figure(figsize=(10, 5))
# plt.plot(new_time, audio_frames3[1])
# plt.title(f"Frames of 32ms")
# plt.xlabel("Time [s]")
# plt.ylabel("Amplitude")
# plt.show()

for i in range(0, len(audio_frames3)):
    plt.figure(figsize=(10, 5))
    plt.plot(new_time, audio_frames3[i])
    plt.title(f"Frames of 32ms")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
plt.show()


# plot_signal_with_frames_discrete(audio_frames, frequency_audio, 0.32)
# plot_signal_with_frames_discrete(audio_frames, frequency_audio, 0.32)