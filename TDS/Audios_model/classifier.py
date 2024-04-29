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

from utils import cut_signal_frames, convert_m4a_to_wav, detect_voice_activity, process_voice_activity

in_path_audios_m4a = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/In_audios_m4a/"
in_path_audios = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/In_audios_wav/"
out_path_audios = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/Out_audios"
path_base = "/Users/oscarjimenezbou/Library/Mobile Documents/com~apple~CloudDocs/Documents/University_projects/TDS/Audios_model/audios"    

persons = [("Oscar", 1), ("Marta", 2), ("Isabel", 3), ("Abuela", 4), ("Papa", 5)]
numbers_records = [1, 2, 3, 4]
numbers = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"]

choosen_person = int(input("Choose the number: 1.Oscar, 2.Marta, 3.Isabel, 4.Abuela, 5.Papa\n"))
choosen_version = int(input("Choose the record: 1, 2, 3, 4\n"))

audio_name = f"audio{persons[choosen_person-1][0]}{numbers_records[choosen_version-1]}"

try:
    convert_m4a_to_wav(in_path_audios_m4a, output_path=in_path_audios)
except:
    None
    
frecuency_audio, audio_raw = wavfile.read(in_path_audios + f"{audio_name}.wav") # freqcuency_audio = 44100

#convert the audio signal to mono
if len(audio_raw.shape) > 1:
    audio_data = audio_raw[:, 0]
        
#normalize the audio signal and apply a gain of 0.8
audio_raw = audio_raw / np.max(np.abs(audio_raw))

ganancia = 0.75  
audio_raw *= ganancia

#reseample the audio signal to 16000 Hz
audio_raw = signal.resample(audio_raw, int(len(audio_raw) * 16000 / frecuency_audio))

#trim the audio signal
audio, index = librosa.effects.trim(
    audio_raw, top_db=20, frame_length=2048, hop_length=512)

#add silence 0.5s
silence = np.zeros(int(0.5 * 16000))
audio = np.concatenate((silence, audio, silence)) 

#pick the first 10 numbers from the audio signal


###########################Run the VAD algorithm################################

voice_activity, audio_frames = detect_voice_activity(audio, frecuency=16000, threshold=0.015)
process_voice_activity(voice_activity, audio_frames, out_path_audios, numbers_list=numbers, silence_before_after=0.5)

#preguntar por la terminal si hacer los siguientes plots
answer = input("Do you want to make audio plots? Y/N: \n")

if answer == "Y" or answer == "y":
    plt.figure(figsize=(10, 5))
    plt.plot(voice_activity)
    plt.show()
    for i in range(10):
        freq, ad = wavfile.read(out_path_audios+f"/{numbers[i]}.wav") 
        print(f"Maximum amplitud of Audio {numbers[i]} is: {np.max(np.abs(ad))}")
        plt.figure(figsize=(10, 5))
        plt.plot(ad)
        plt.title(f"Audio {numbers[i]}")
        plt.xlabel("Muestras")
        plt.show()
else:
    # for i in range(10):
    #     freq, ad = wavfile.read(out_path_audios+f"/{numbers[i]}.wav") 
    #     print(f"Maximum amplitud of Audio {numbers[i]} is: {np.max(np.abs(ad))}")
    # plt.figure(figsize=(10, 5))
    # plt.plot(voice_activity)
    # plt.show()
    print("Goodbye!")


answer = input("Do you want to move the audio to final folder? Y/N: \n")

if answer == "Y" or answer == "y":
    for number in numbers:
        os.rename(out_path_audios + "/" + number + ".wav", path_base + "/" + number + "/" +f"{number}_{persons[choosen_person-1][1]}_{numbers_records[choosen_version-1]}.wav")
else:
    None
    