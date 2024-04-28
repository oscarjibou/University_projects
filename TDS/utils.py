import os
import sys
import numpy as np
import pydub
import scipy.signal as signal
import glob

from numpy.typing import ArrayLike
from matplotlib import pyplot as plt
from scipy.signal import get_window
from scipy.io import wavfile
from scipy.io.wavfile import write, read
from pydub import AudioSegment
from vad import EnergyVAD

epsilon = sys.float_info.epsilon

def continuous_time_plot(*args: ArrayLike, variable_name: str, xlabel="Time (s)"):

    plt.figure(figsize=(10, 5))
    plt.plot(*args)
    plt.title("Señal en el dominio del tiempo continuo")
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.show()

def discrete_time_plot(*args: ArrayLike, variable_name: str, xlabel="Time (s)"):

    plt.figure(figsize=(10, 5))
    plt.stem(*args)
    plt.title("Señal en el dominio del tiempo discreto")
    plt.xlabel("Muestras [n]")
    plt.ylabel("Amplitud")
    plt.show()

#fuction to cut the signal in 32ms frames
# def cut_signal_frames(señal, frecuencia_señal, tiempo_frames=0.032):
#     frames_signal = []
#     for i in range(0, len(señal), int(frecuencia_señal * tiempo_frames)):
#         frames_signal.append(señal[i:i + int(frecuencia_señal * tiempo_frames)]) 
#     return frames_signal   

def cut_signal_frames(señal, frecuencia_señal, tiempo_frames=0.032, overlap=0):
    frames_signal = []
    frame_size = int(frecuencia_señal * tiempo_frames)
    step_size = int(frame_size * (1 - overlap))
    
    # for i in range(0, len(señal), frame_size):
    #     # Convertir cada frame a lista antes de añadirlo
    #     frames_signal.append(list(señal[i:i + frame_size]))
    # return frames_signal
    
    for i in range(0, len(señal) - frame_size + 1, step_size):
    # Convertir cada frame a lista antes de añadirlo
        frames_signal.append(list(señal[i:i + frame_size]))

    return frames_signal
    

def plot_signal_with_frames_time(señal_in_frames, frecuencia_señal, tiempo_señal, tiempo_frames=0.032):
    plt.figure(figsize=(10, 5))
    for i, frame in enumerate(señal_in_frames):
        plt.plot(tiempo_señal[i * int(tiempo_frames * frecuencia_señal): (i+1) * int(tiempo_frames * frecuencia_señal)], frame)
    plt.title(f"Frames of {tiempo_frames*1000}ms")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    return plt.show()


def split_signal_into_frames(
    signal, sample_rate, window_size, window_overlap, window_type="hann"
):
    """
    Split the signal into frames using a sliding window approach
    Args:
    signal (np.array): The input signal
    sample_rate (int): The sample rate of the signal
    window_size (float): The size of the window in SECONDS
    window_overlap (float): The overlap between consecutive windows in seconds
    window_type (str): The type of window to use

    Returns:
    np.array: The signal split into frames
    """
    window_length = int(window_size * sample_rate)
    step_size = window_length - int(window_overlap * sample_rate)
    window = get_window(window_type, window_length)
    num_frames = int(np.ceil(float(np.abs(len(signal) - window_length)) / step_size))

    # Zero padding at the end to make sure that all frames have equal number of samples
    # without truncating any part of the signal
    pad_signal_length = num_frames * step_size + window_length
    z = np.zeros((pad_signal_length - len(signal)))
    pad_signal = np.append(signal, z)  # Pad signal

    indices = (
        np.tile(np.arange(0, window_length), (num_frames, 1))
        + np.tile(np.arange(0, num_frames * step_size, step_size), (window_length, 1)).T
    )
    frames = pad_signal[indices.astype(np.int32, copy=False)]

    # Apply the window function to each frame
    windowed_frames = frames * window

    return windowed_frames

def number_count_detector(
    signal, sample_rate, window_size, window_overlap, count=10, margin=0.02
):
    """
    Detects the presence of voice in a number count using a simple energy-based approach

    Args:
    signal (np.array): The input signal
    sample_rate (int): The sample rate of the signal
    window_size (float): The size of the window in seconds
    window_overlap (float): The overlap between consecutive windows in seconds
    count (int): The number of numbers to detect
    margin (float): The safety margin of seconds to add to the detected voice
    
    Returns:
    np.array: A binary array indicating the presence of voice
    """
    # Split the signal into frames
    windowed_frames = split_signal_into_frames(
        signal, sample_rate, window_size, window_overlap
    )
    window_samples = round(window_size * sample_rate)
    count_flag = False

    thresholds = []

    # Calculating the energy of each frame
    energy = np.sum(windowed_frames**2, axis=1)

    # Finding the threshold that gives the correct number of numbers detected
    for thres in np.arange(1000):
        count_numbers = 0
        threshold = (thres / 1000) * np.max(energy)
        vad = (energy > threshold).astype(int)  # Voice Activity Detection
        voice = np.repeat(
            vad, window_samples
        )  # Repeat the voice detection to match the signal length

        # Counting the number of numbers detected
        for i in range(len(voice)):
            if voice[i] == 1 and voice[i - 1] == 0:
                count_numbers += 1

        if count_numbers == count and count_flag == False:
            count_flag = True
            thresholds.append(thres)

        elif count_numbers > count:
            thresholds.append(thres)
            break

    print(f"Thresholds used: {thresholds}")
    threshold = (np.median(thresholds) / 100) * np.max(energy)
    vad = (energy > threshold).astype(int)
    voice = np.repeat(vad, window_samples)
    print(f"Threshold used: {np.median(thresholds) / 100}")
    # Counting the number of numbers detected
    count_numbers = 0
    for i in range(len(voice)):
        if voice[i] == 1 and voice[i - 1] == 0:
            count_numbers += 1
    print(f"Number of numbers detected: {count_numbers}")
    print(f"Maximum amplitude: {np.max(signal)}")

    # Now adding a safety margin to the detected voice
    safety_margin = int(margin * sample_rate)

    # Find the start and end indices of each voice segment
    voice_segments = np.where(np.diff(voice))[0] + 1

    # Add the safety margin to these indices
    for start in voice_segments[::2]:
        voice[max(0, start - safety_margin) : start] = 1
    for end in voice_segments[1::2]:
        voice[end : min(len(voice), end + safety_margin)] = 1

    return voice

def export_numbers(signal, sample_rate, voice, count=10, output_path=any
                   ):
    """
    Exports the detected numbers in the signal to individual wav files

    Args:
    signal (np.array): The input signal
    sample_rate (int): The sample rate of the signal
    voice (np.array): A binary array indicating the presence of voice
    count (int): The number of numbers to detect
    output_path (str): The path to save the detected numbers
    """
    # Find the start and end indices of each voice segment
    voice_segments = np.where(np.diff(voice))[0] + 1

    # Make sure we have an even number of indices
    if len(voice_segments) % 2 != 0:
        voice_segments = np.append(voice_segments, len(voice))

    # Export each voice segment to a separate wav file
    for i in range(0, min(len(voice_segments), 2 * count), 2):
        start, end = voice_segments[i], voice_segments[i + 1]
        write(f"{output_path}{i//2}.wav", sample_rate, signal[start:end])


def convert_m4a_to_wav(input_path, output_path):  
    '''
    before using this function, you need to install ffmpeg (brew install ffmpeg)
    
    M4A to WAV conversion function and move the files to the output path
    After DELETE the M4A files
    
    args:
    input_path: string, path to the input audio files
    output_path: string, path to save the output audio files
    '''
    
    audio_dir = input_path
    extension_list = ('*.m4a',)  # Filter only M4A files

    os.chdir(audio_dir)
    for extension in extension_list:
        for audio in glob.glob(extension):
            wav_filename = os.path.splitext(os.path.basename(audio))[0] + '.wav'
            # Load the M4A file and export it as WAV
            AudioSegment.from_file(audio, format='m4a').export(wav_filename, format='wav')
            # Move the file to the output path
            os.rename(wav_filename, output_path+"/"+wav_filename)
            # Delete the M4A file
            os.remove(audio)
            
def detectar_actividad_vocal(audio, frecuency=16000, threshold=0.015, tiempo_frames=0.032, overlap=0):
    '''
    Args:
    audio: numpy array, audio signal
    frecuency: int, frecuency of the audio signal
    threshold: float, energy threshold
    tiempo_frames: float, time of the frames
    overlap: float, overlap between frames
    
    Returns:
    voice_activity: numpy array, voice activity
    audio_frames: numpy array, audio frames
    '''
    # Create the VAD object
    vad = EnergyVAD(frecuency,frame_length=60,frame_shift=32, energy_threshold=threshold) 
    # Get the voice activity
    voice_activity = vad(audio)
    # Cut the signal into frames
    audio_frames = cut_signal_frames(audio, frecuency, tiempo_frames, overlap)
    samples = cut_signal_frames([i for i in range(len(audio))], frecuency, tiempo_frames, overlap)

    for i in range(len(voice_activity)):
        if voice_activity[i] == 1:
            audio_frames[i] = audio_frames[i]
            samples[i] = samples[i]
        else:
            audio_frames[i] = np.zeros(np.shape(audio_frames[i]))
            samples[i] = np.zeros(np.shape(samples[i]))
                
    return voice_activity, audio_frames

def procesar_actividad_vocal(voice_activity, audio_frames, path_base, numbers_list, numbers_count=10, 
                             silence_before_after = 0.5, error_margin = 2):
    '''
    Fuction to process the voice activity and save the audio frames
    
    Args:
    voice_activity: numpy array, voice activity
    audio_frames: numpy array, audio frames
    path_base: string, path to save the audio frames
    numbers_list: list, list of number names to be saved
    numbers_count: int, number of audio frames to save
    silence_before_after: float, silence before and after the audio frames
    error_margin: int, margin of error to detect the audio frames
    
    Returns:
    None
    '''
    
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
                    file_path = f"{path_base}/{numbers_list[index_number]}.wav"
                    # Concatenate the audio frames into a single audio
                    audio_no_frames = np.concatenate(audio_frames[inicio:final])
                    # Add silence before and after the audio
                    audio_silencio = np.concatenate([np.zeros(int(silence_before_after*16000)) 
                                                     ,audio_no_frames, np.zeros(int(silence_before_after * 16000))])
                    # Save the audio file
                    write(file_path, 16000, audio_silencio)
                    index_number += 1
                else:
                    break
        elif voice_activity[i] == 1:
            inicio = i - error_margin
            detectado = True

def spectral_centroid_spread(fft_magnitude, sampling_rate):
    '''
    github link: https://github.com/tyiannak/pyAudioAnalysis/blob/master/pyAudioAnalysis/ShortTermFeatures.py

    functions: spectral_centroid_spread, spectral_flux
    '''
    """
    Computes spectral centroid of frame (given abs(FFT)) and spread of the frame.
    It provides an idea of where the "brightness" or "density" of a sound signal is concentrated. 
    It indicates the "center of gravity" of the frequency spectrum of a signal
    
    ARGUMENTS:
        fft_magnitude:            abs(FFT) of the signal
        sampling_rate:            the sampling freq (needed to obtain the frequency vector)
        
    RETURNS:    
        a tuple (centroid, spread)
        centroid:    spectral centroid
        spread:        spectral spread
    """
    ind = (np.arange(1, len(fft_magnitude) + 1)) * \
          (sampling_rate / (2.0 * len(fft_magnitude)))

    Xt = fft_magnitude.copy()
    Xt_max = Xt.max()
    if Xt_max == 0:
        Xt = Xt / epsilon
    else:
        Xt = Xt / Xt_max

    NUM = np.sum(ind * Xt)
    DEN = np.sum(Xt) + epsilon

    # Centroid:
    centroid = (NUM / DEN)

    # Spread:
    spread = np.sqrt(np.sum(((ind - centroid) ** 2) * Xt) / DEN)

    # Normalize:
    centroid = centroid / (sampling_rate / 2.0)
    spread = spread / (sampling_rate / 2.0)

    return centroid, spread

def spectral_flux(fft_magnitude, previous_fft_magnitude):
    """
    Measures the amount of change in the power spectrum of a signal from one frame to another
    Must to use frame by frame (not in the whole signal)
    ARGUMENTS:
        fft_magnitude:            the abs(fft) of the current frame
        previous_fft_magnitude:        the abs(fft) of the previous frame
    """
    '''
    
    '''
    # compute the spectral flux as the sum of square distances:
    fft_sum = np.sum(fft_magnitude + epsilon)
    previous_fft_sum = np.sum(previous_fft_magnitude + epsilon)
    sp_flux = np.sum(
        (fft_magnitude / fft_sum - previous_fft_magnitude /
         previous_fft_sum) ** 2)

    return sp_flux

