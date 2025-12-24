# Procesamiento Digital de Señales - Audio

Este repositorio contiene un proyecto completo de procesamiento digital de señales enfocado en el análisis y procesamiento de señales de audio. El proyecto incluye prácticas que cubren desde conceptos básicos de señales hasta clasificación de audio mediante redes neuronales profundas.

## 📋 Descripción del Proyecto

Este proyecto está estructurado en múltiples prácticas que abordan diferentes aspectos del procesamiento de señales de audio:

- **Análisis de señales en tiempo continuo y discreto**
- **Detección de actividad de voz (VAD)**
- **Extracción de características espectrales**
- **Clasificación de números hablados en español**
- **Redes neuronales para reconocimiento de voz**

## 📁 Estructura del Proyecto

```
signal_digital_processing/
├── P1/                    # Práctica 1: Análisis básico de señales
│   ├── src.ipynb         # Notebook principal
│   ├── sound*.wav        # Archivos de audio de ejemplo
│   └── Practicas_Practica1_Practica1.pdf
│
├── P2/                    # Práctica 2: Análisis de energía y tramas
│   ├── src.ipynb         # Notebook principal
│   ├── soundOscar.wav    # Audio de voz
│   └── Practica2.pdf
│
├── P3/                    # Práctica 3: Análisis espectral
│   ├── src.ipynb         # Notebook principal
│   └── Practica3.pdf
│
├── P4/                    # Práctica 4: Extracción de características
│   ├── src.ipynb         # Notebook principal
│   └── Practica4.pdf
│
├── P5/                    # Práctica 5: Clasificación con características
│   ├── src.ipynb         # Notebook principal
│   ├── practica5.ipynb
│   ├── train_spanish_2022_python.mat
│   ├── validation_spanish_2022_python.mat
│   └── Practica5.pdf
│
├── P6/                    # Práctica 6: Redes neuronales para audio
│   ├── practica6.ipynb   # Notebook principal
│   ├── train_net.py      # Script de entrenamiento
│   ├── utils.py          # Utilidades específicas de P6
│   └── base_datos_numeros_2023_AB/  # Dataset de números
│       ├── train/        # 12,812 archivos WAV
│       ├── test/         # 3,082 archivos WAV
│       └── notas.csv
│
├── Audios_model/          # Modelo de clasificación de números
│   ├── classifier.py     # Clasificador de números hablados
│   ├── audios/           # Audios organizados por número (0-9)
│   ├── In_audios_wav/    # Audios de entrada en formato WAV
│   ├── In_audios_m4a/    # Audios de entrada en formato M4A
│   └── Out_audios/       # Audios procesados
│
├── Grader/                # Funciones MATLAB para evaluación
│   ├── bloque0/          # Funciones básicas
│   └── bloque1/          # Funciones de procesamiento
│
└── utils.py              # Funciones auxiliares compartidas
```

## 🛠️ Funcionalidades Principales

### Módulo `utils.py`

El archivo `utils.py` contiene funciones auxiliares para el procesamiento de audio:

- **`cut_signal_frames()`**: Divide señales en tramas con solape configurable
- **`split_signal_into_frames()`**: Segmentación de señales con ventanas
- **`number_count_detector()`**: Detección de números hablados mediante energía
- **`detect_voice_activity()`**: Detección de actividad de voz (VAD)
- **`export_numbers()`**: Exportación de números detectados a archivos WAV
- **`convert_m4a_to_wav()`**: Conversión de formato M4A a WAV
- **`spectral_centroid_spread()`**: Cálculo de centroide y dispersión espectral
- **`spectral_flux()`**: Medida de cambio en el espectro
- **`spectral_rolloff()`**: Cálculo del rolloff espectral

### Clasificador de Números (`Audios_model/classifier.py`)

Sistema para procesar y clasificar números hablados del 0 al 9 en español:
- Conversión de M4A a WAV
- Resampleo a 16 kHz
- Detección de actividad de voz
- Segmentación automática de números
- Organización de audios por número y persona

### Práctica 6: Red Neuronal

Implementación de una red neuronal convolucional para clasificación de números:
- Preprocesamiento de audio (espectrograma mel)
- Entrenamiento con PyTorch
- Dataset de números en español (2023)

## 📦 Dependencias

Las principales librerías utilizadas en el proyecto son:

```python
numpy              # Operaciones numéricas
scipy              # Procesamiento de señales
matplotlib         # Visualización
librosa            # Análisis de audio
pydub              # Manipulación de audio
torch              # Deep learning (P6)
sounddevice        # Grabación/reproducción de audio
simpleaudio        # Reproducción simple de audio
tqdm               # Barras de progreso
pandas             # Manipulación de datos
```

### Instalación

Para instalar las dependencias, puedes usar:

```bash
pip install numpy scipy matplotlib librosa pydub torch sounddevice simpleaudio tqdm pandas
```

**Nota**: Para la conversión de M4A a WAV, necesitarás tener instalado `ffmpeg`:

```bash
# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg

# Windows
# Descargar desde https://ffmpeg.org/download.html
```

## 🚀 Uso

### Práctica 1: Análisis Básico de Señales

```python
from scipy.io import wavfile
from utils import continuous_time_plot, discrete_time_plot

frecuencia, datos = wavfile.read('sound1.wav')
# Análisis y visualización de señales
```

### Práctica 2: Análisis de Energía

```python
from utils import cut_signal_frames

frames = cut_signal_frames(señal, frecuencia_muestreo, tiempo_frames=0.032)
# Cálculo de energía por tramas
```

### Clasificador de Números

```python
python Audios_model/classifier.py
# El script interactivo te permitirá:
# 1. Seleccionar una persona (Oscar, Marta, Isabel, Abuela, Papa)
# 2. Seleccionar una grabación (1-4)
# 3. Procesar y segmentar los números del audio
```

### Práctica 6: Entrenamiento de Red Neuronal

```python
# Desde el directorio P6
python train_net.py
# O abrir el notebook practica6.ipynb
```

## 📊 Datasets

### Dataset de Números (P6)
- **Entrenamiento**: 12,812 archivos WAV
- **Prueba**: 3,082 archivos WAV
- **Clases**: Números del 0 al 9 en español
- **Formato**: WAV, 16 kHz (estimado)

### Audios de Entrenamiento (Audios_model)
- Audios organizados por número (cero, uno, dos, ..., nueve)
- Múltiples grabaciones por persona
- Formato: WAV, 16 kHz

## 🔬 Características Extraídas

El proyecto implementa la extracción de múltiples características espectrales:

- **Centroide espectral**: Indica la "brillantez" del sonido
- **Dispersión espectral**: Mide la concentración del espectro
- **Flujo espectral**: Cambio en el espectro entre tramas
- **Rolloff espectral**: Frecuencia donde se concentra la energía
- **Energía por tramas**: Energía en ventanas temporales

## 📝 Notas

- Los archivos PDF en cada práctica contienen las especificaciones y requisitos
- Los notebooks están diseñados para ejecutarse en orden (P1 → P6)
- El módulo `utils.py` es compartido entre todas las prácticas
- Los audios de ejemplo están incluidos en cada práctica

## 🎯 Objetivos de Aprendizaje

Este proyecto cubre:

1. **Fundamentos de señales**: Tiempo continuo vs discreto, muestreo
2. **Análisis temporal**: Energía, potencia, tramas
3. **Análisis frecuencial**: FFT, espectrogramas, características espectrales
4. **Procesamiento de voz**: VAD, segmentación, normalización
5. **Machine Learning**: Extracción de características, clasificación
6. **Deep Learning**: Redes neuronales para audio, espectrogramas mel

## 📄 Licencia

Este es un proyecto académico para fines educativos.

## 👤 Autor

Proyecto desarrollado como parte del curso de Procesamiento Digital de Señales.

---

**Nota**: Asegúrate de tener todos los archivos de audio necesarios antes de ejecutar las prácticas. Algunos archivos pueden requerir rutas específicas que deberás ajustar según tu configuración.

