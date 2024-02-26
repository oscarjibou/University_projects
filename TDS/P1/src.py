import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import simpleaudio as sa


archivo_wav = 'sound1.wav'

# Load a wave file and play it
wave_obj = sa.WaveObject.from_wave_file(archivo_wav)
play_obj = wave_obj.play()
play_obj.wait_done()

#plot the wave file in discrete time
frecuencia_muestreo, datos = wavfile.read(archivo_wav)

# Crear el eje de tiempo. El número de datos dividido por la frecuencia de muestreo nos da el tiempo total de la grabación.
tiempo = 1/frecuencia_muestreo * np.arange(0, len(datos))

# Graficar el archivo WAV en tiempo discreto
plt.figure(figsize=(12, 6))
plt.plot(tiempo, datos)
plt.title('Señal de audio en tiempo discreto')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.show()

