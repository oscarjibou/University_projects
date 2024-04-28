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
from scipy.io.wavfile import write

from utils import cut_signal_frames

path = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/In_audios/"

frecuency_audio, audio_raw = wavfile.read(path + "prueba2.wav") # freqcuency_audio = 44100

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
vad = EnergyVAD(16000,frame_length=60,frame_shift=32, energy_threshold=0.015) 

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
numbers = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez"]

def procesar_actividad_vocal(voice_activity, audio_frames, path_base, numbers_count=10, margin=2):
    index_number = 0
    detectado = False
    inicio, final = 0, 0

    for i in range(len(voice_activity)):
        if detectado:
            if voice_activity[i] == 1:
                final = i
            elif voice_activity[i] == 0:
                detectado = False
                if index_number <= (numbers_count - 1) :
                    file_path = f"{path_base}/{numbers[index_number]}.wav"
                    write(file_path, 16000, np.concatenate(audio_frames[inicio:final]))
                    index_number += 1
                else:
                    break
        elif voice_activity[i] == 1:
            inicio = i - margin
            detectado = True

# Ejemplo de cómo llamar a la función
path_base = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/Out_audios"
procesar_actividad_vocal(voice_activity, audio_frames, path_base)

for i in range(10):
    freq, ad = wavfile.read(path_base+f"/{numbers[i]}.wav") 
    plt.figure(figsize=(10, 5))
    plt.plot(ad)
    plt.title(f"Audio {numbers[i]}")
    plt.xlabel("Muestras")
    plt.show()