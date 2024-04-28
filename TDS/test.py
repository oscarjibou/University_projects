import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import scipy.signal as signal
import librosa
import simpleaudio as sa

sys.path.append("/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS")


from vad import EnergyVAD
from scipy.io import wavfile
from scipy.io.wavfile import write, read

from utils import number_count_detector, export_numbers, cut_signal_frames

path = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/In_audios/"

frecuency_audio, audio_raw = wavfile.read(path + "hh.wav") # freqcuency_audio = 44100

#cut the audio to 80000 samples
# audio_raw = audio_raw[:80000]

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
vad = EnergyVAD(16000,frame_length=50,frame_shift=32, energy_threshold=0.05) 

voice_activity = vad(audio)

audio_frames = cut_signal_frames(audio, 16000, tiempo_frames=0.032, overlap=0)
samples = cut_signal_frames([i for i in range(len(audio))], 16000, tiempo_frames=0.032, overlap=0)

for i in range(len(voice_activity)):
    if voice_activity[i] == 1:
        audio_frames[i] = audio_frames[i]
        samples[i] = samples[i]
    else:
        audio_frames[i] = np.zeros(np.shape(audio_frames[i]))
        samples[i] = np.zeros(np.shape(samples[i]))
        
##################
print(type(audio_frames[0]))

numbers = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]
detect = 0
index_number = 0

for i in range(len(voice_activity)):
    if voice_activity[i] == 1 and detect == 1:
        final = i
        
    elif detect == 1 and voice_activity[i] == 0:
        detect = 0
        write(f"/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/Out_audios/{numbers[indice_numero]}.wav", 16000, np.concatenate(audio_frames[inicio:final]))
        index_number += 1  
            
    elif detect == 0:
        if voice_activity[i] == 1:
            inicio = i - 6
            detect = 1
    
    else:
        pass

print(audio_frames[15:40])
        



# ##################

# #convert the result audio_frames to a numpy array
# audio_frames = np.concatenate(audio_frames)

# #convert the result audio_frames to file .wav
# write("/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/Out_audios/voice_activity.wav", 16000, audio_frames)
