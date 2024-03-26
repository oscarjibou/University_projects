from matplotlib import pyplot as plt
from numpy.typing import ArrayLike


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