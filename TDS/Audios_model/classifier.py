import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import scipy.signal as signal
import librosa
import simpleaudio as sa

sys.path.append("/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS")

from scipy.io import wavfile
from scipy.io.wavfile import write, read

from utils import number_count_detector, export_numbers

path = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/In_audios/"

frecuency_audio, audio_raw = wavfile.read(path + "oscar.wav") # freqcuency_audio = 44100

#convert the audio signal to mono
if len(audio_raw.shape) > 1:
    audio_data = audio_raw[:, 0]
        
#normalize the audio signal and apply a gain of 0.8
audio_raw = audio_raw / np.max(np.abs(audio_raw))

ganancia = 0.8  
audio_raw *= ganancia

#reseample the audio signal to 16000 Hz
audio_raw = signal.resample(audio_raw, int(len(audio_raw) * 16000 / frecuency_audio))

#trim the audio signal
audio, index = librosa.effects.trim(
    audio_raw, top_db=20, frame_length=2048, hop_length=512)

#add silence 0.5s
silence = np.zeros(int(0.5 * 16000))
audio = np.concatenate((silence, audio, silence)) 

#find if the audio is above 0.97 amplitude
print("Maximum amplitude:", np.max(np.abs(audio)))

#pick the first 10 numbers from the audio signal
numbers_vad = number_count_detector(
    audio,
    16000,
    window_size=0.02,
    window_overlap = 0,
    count=10,
)

# Cut the audio signal into individual numbers
path_out = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/Out_audios/"

export_numbers(
    audio,
    16000,
    numbers_vad,
    count=10,
    output_path=path_out,
    )

plt.figure(figsize=(10, 6))
plt.plot(audio)
plt.plot(numbers_vad)
plt.show()



frecuency_audio2, audio_raw2 = wavfile.read("/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/Out_audios/0.wav") # freqcuency_audio = 44100    

print(frecuency_audio2)
