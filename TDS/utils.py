from matplotlib import pyplot as plt
from numpy.typing import ArrayLike
import numpy as np
from scipy.signal import get_window
from scipy.io import wavfile
import pydub
import scipy.signal as signal
from scipy.io.wavfile import write, read


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
def cut_signal_frames(señal, frecuencia_señal, tiempo_frames=0.032):
    frames_signal = []
    for i in range(0, len(señal), int(frecuencia_señal * tiempo_frames)):
        frames_signal.append(señal[i:i + int(frecuencia_señal * tiempo_frames)]) 
    return frames_signal   

def plot_signal_with_frames(señal_in_frames, frecuencia_señal, tiempo_señal, tiempo_frames=0.032):
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
    window_size (float): The size of the window in seconds
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


def m4a_to_wav(m4a_file, wav_file):
    """
    Convert an m4a file to a wav file

    Args:
    m4a_file (str): The path to the m4a file
    wav_file (str): The path to save the wav file
    """

    sound = pydub.AudioSegment.from_file(m4a_file)
    sound.export(wav_file, format="wav")

    # Read the audio file
    freq, audio_data = wavfile.read(wav_file)
    print(f"Audio frequency: {freq}Hz")

    # Now we will make the audio Mono
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)
        print("Audio is stereo, converting to mono")

    audio_data = audio_data / 2**15 # Normalizing the audio data

    # Normalization (if your audio data is in integers and needs to be normalized)
    # audio_data = audio_data / np.max(np.abs(audio_data))

    # Changing the audio frequency to 16kHz if necesary
    # Target frequency
    target_freq = 16000

    if freq != 16000:
        print(f"Resampling audio from {freq}Hz to {target_freq}Hz")
        # Calculate new length of the sample
        new_length = round(len(audio_data) * target_freq / freq)

        # Resample the audio to the target frequency
        audio_data = signal.resample(audio_data, new_length)
    return audio_data, freq, target_freq

def export_numbers(signal, sample_rate, voice, count, output_path):
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

