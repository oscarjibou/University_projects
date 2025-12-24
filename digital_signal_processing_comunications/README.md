# Procesamiento Digital de Señales y Comunicaciones

Este repositorio contiene un proyecto completo de procesamiento digital de señales enfocado en técnicas de codificación, compresión y transformación de señales de audio e imágenes. El proyecto cubre desde conceptos básicos de procesamiento hasta técnicas avanzadas de compresión sin pérdidas y transformadas.

## 📋 Descripción del Proyecto

Este proyecto está estructurado en múltiples prácticas que abordan diferentes aspectos del procesamiento digital de señales y comunicaciones:

- **Procesamiento básico de audio**: Lectura, reproducción y análisis de señales de audio
- **Codificación de imágenes**: Conversión de imágenes a formato binario (escala de grises y RGB)
- **Codificación PCM**: Modulación por código de pulsos para audio
- **Compresión sin pérdidas**: Codificación Rice y predicción para imágenes
- **Transformada DCT**: Transformada Discreta del Coseno aplicada a bloques de audio

## 📁 Estructura del Proyecto

```
digital_signal_processing_comunications/
├── P1/                    # Práctica 1: Procesamiento básico de audio
│   ├── P1.ipynb          # Notebook principal
│   ├── P1.py             # Script Python
│   └── l1.pdf            # Enunciado de la práctica
│
├── P2/                    # Práctica 2: Codificación de imágenes
│   ├── P2.ipynb          # Notebook principal
│   ├── code.py           # Funciones de codificación/decodificación
│   ├── 1i.bin            # Imagen codificada (escala de grises)
│   ├── 1i_rgb.bin        # Imagen codificada (RGB)
│   └── l2.pdf            # Enunciado de la práctica
│
├── P3/                    # Práctica 3: Codificación PCM
│   ├── P3.ipynb          # Notebook principal
│   ├── code.py           # Funciones PCM (codPCM, decPCM)
│   ├── vt1_pcm.bin       # Audio codificado en PCM
│   └── l3.pdf            # Enunciado de la práctica
│
├── P4/                    # Práctica 4: Compresión sin pérdidas (Rice)
│   ├── P4.ipynb          # Notebook principal
│   ├── i1_pred.bin       # Imagen comprimida con predicción
│   ├── i1_rec.png        # Imagen reconstruida
│   └── l4.pdf            # Enunciado de la práctica
│
├── P5/                    # Práctica 5: Transformada DCT y filtrado
│   ├── P5.ipynb          # Notebook principal
│   ├── code.py           # Funciones DCT y filtrado
│   └── l5.pdf            # Enunciado de la práctica
│
└── data/                  # Archivos de datos
    ├── clarinete.wav     # Audio de ejemplo
    ├── v1.wav            # Audio de voz
    ├── v4.wav            # Audio de voz
    ├── vt1.wav           # Audio de voz
    ├── v_e.wav           # Audio de entrada
    ├── v_s.wav           # Audio de salida
    ├── i1.png            # Imagen de ejemplo
    ├── i2.png            # Imagen de ejemplo
    ├── i3.png            # Imagen de ejemplo
    └── i4.png            # Imagen de ejemplo
```

## 🛠️ Funcionalidades por Práctica

### Práctica 1: Procesamiento Básico de Audio

**Objetivo**: Introducción al procesamiento de señales de audio.

**Funcionalidades**:
- Lectura de archivos WAV
- Reproducción de audio
- Visualización de señales en el dominio del tiempo
- Normalización de señales
- Análisis de propiedades del audio (frecuencia de muestreo, canales, profundidad de bits)

**Ejemplo de uso**:
```python
import scipy.io.wavfile as wav
import sounddevice as sd

fs, audio_data = wav.read("v1.wav")
sd.play(audio_data, fs)
sd.wait()
```

### Práctica 2: Codificación de Imágenes

**Objetivo**: Implementación de funciones para codificar y decodificar imágenes en formato binario.

**Funciones principales**:
- `escribeIm()`: Codifica imagen en escala de grises a binario
- `leeIm()`: Decodifica imagen en escala de grises desde binario
- `escribeRGB()`: Codifica imagen RGB a binario
- `leeRGB()`: Decodifica imagen RGB desde binario
- `rgb_to_y()`: Conversión RGB a luminancia (Y)

**Características**:
- Soporte para imágenes en escala de grises y RGB
- Formato binario con cabecera (dimensiones + datos)
- Almacenamiento por columnas (compatible con MATLAB)
- Conversión RGB a escala de grises usando pesos estándar (0.299R + 0.587G + 0.114B)

**Ejemplo de uso**:
```python
from PIL import Image
import numpy as np

# Codificar imagen en escala de grises
im = Image.open("i1.png").convert("L")
x = np.array(im, dtype=np.uint8)
escribeIm(x, "1i.bin")

# Decodificar
y = leeIm("1i.bin")
```

### Práctica 3: Codificación PCM (Pulse Code Modulation)

**Objetivo**: Implementación de codificación PCM para señales de audio.

**Funciones principales**:
- `codPCM(x, R, fi)`: Codifica señal de audio usando R bits por muestra
- `decPCM(fi)`: Decodifica señal PCM desde archivo binario

**Características**:
- Cuantización uniforme con paso Δ = 2^(1-R)
- Almacenamiento de parámetros en cabecera (R, número de muestras)
- Cálculo de error cuadrático medio (MSE)
- Reproducción de señales originales y decodificadas para comparación

**Parámetros**:
- `R`: Número de bits por muestra (resolución de cuantización)
- `x`: Señal de entrada normalizada en [-1, 1]
- `fi`: Nombre del archivo binario de salida

**Ejemplo de uso**:
```python
import soundfile as sf

x, fs = sf.read("vt1.wav")
R = 13  # bits por muestra
codPCM(x, R, "vt1_pcm.bin")

y, R_leido = decPCM("vt1_pcm.bin")
mse = np.mean((x - y) ** 2)
```

### Práctica 4: Compresión Sin Pérdidas con Codificación Rice

**Objetivo**: Implementación de codificación predictiva sin pérdidas usando código Rice.

**Funciones principales**:
- `rice_encode(e, m)`: Codifica entero usando código Rice-m
- `rice_decode(bitstream, m, pos_inicial)`: Decodifica código Rice-m
- `codPred(nombreI, nombreS, m)`: Codifica imagen con predicción y Rice
- `decPred(nombreS, nombreI)`: Decodifica imagen comprimida

**Características**:
- Predicción de primera diferencia (diferencia entre píxeles consecutivos)
- Codificación Rice-m para errores de predicción
- Transformación de enteros con signo a enteros positivos
- Código unario para cociente + código binario fijo para resto
- Compresión sin pérdidas (reconstrucción perfecta)

**Parámetros**:
- `m`: Parámetro del código Rice (número de bits para el resto)
- `e`: Error de predicción (entero con signo)

**Ejemplo de uso**:
```python
# Codificar imagen con predicción y Rice-m
codPred("i1.png", "i1_pred.bin", m=4)

# Decodificar
decPred("i1_pred.bin", "i1_rec.png")
```

### Práctica 5: Transformada DCT y Filtrado de Audio

**Objetivo**: Aplicación de la Transformada Discreta del Coseno (DCT) a bloques de audio y filtrado de altas frecuencias.

**Funciones principales**:
- `leer_y_expandir(wavfile, N)`: Lee audio y expande a múltiplo de N
- `dct_bloques(xE, N)`: Calcula DCT por bloques de tamaño N
- `idct_bloques(C)`: Transformada inversa DCT
- `filtrar_altas_freq(C, M)`: Elimina coeficientes de índice >= M
- `calcular_ganancias(X_blocks, C_blocks)`: Calcula ganancia de compactación
- `ganancia_compactacion(array)`: Calcula relación media aritmética/geométrica

**Características**:
- División de señal en bloques de tamaño N (típicamente 64)
- Transformada DCT ortogonal por bloques
- Cálculo de ganancia de compactación (compresión)
- Filtrado de altas frecuencias eliminando coeficientes DCT
- Cálculo de SNR (relación señal-ruido) después del filtrado
- Visualización comparativa de señales originales y filtradas

**Parámetros**:
- `N`: Tamaño del bloque (64 muestras típicamente)
- `M`: Índice máximo de coeficientes DCT a conservar (filtrado)

**Ejemplo de uso**:
```python
# Procesar audio con DCT y filtrado
practica5_ejemplo(wavfile="v1.wav", N=64, M=48)
# M=48 significa conservar solo los primeros 48 coeficientes de 64
```

## 📦 Dependencias

Las principales librerías utilizadas en el proyecto son:

```python
numpy              # Operaciones numéricas y arrays
scipy              # Procesamiento de señales (wavfile, dct, idct)
matplotlib         # Visualización de señales e imágenes
PIL (Pillow)       # Procesamiento de imágenes
soundfile          # Lectura/escritura de archivos de audio
sounddevice        # Reproducción de audio
bitstring          # Manipulación de bits (P4)
scikit-image       # Procesamiento avanzado de imágenes
struct             # Empaquetado/desempaquetado binario
```

### Instalación

Para instalar las dependencias:

```bash
pip install numpy scipy matplotlib pillow soundfile sounddevice bitstring scikit-image
```

## 🚀 Uso General

### Ejecutar Prácticas Individuales

Cada práctica puede ejecutarse de forma independiente:

```bash
# Práctica 1: Procesamiento básico de audio
cd P1
jupyter notebook P1.ipynb

# Práctica 2: Codificación de imágenes
cd P2
python code.py

# Práctica 3: Codificación PCM
cd P3
python code.py

# Práctica 4: Compresión Rice
cd P4
jupyter notebook P4.ipynb

# Práctica 5: DCT y filtrado
cd P5
python code.py
```

### Flujo de Trabajo Típico

1. **P1**: Familiarizarse con el procesamiento básico de audio
2. **P2**: Aprender codificación/decodificación de imágenes
3. **P3**: Implementar codificación PCM y entender cuantización
4. **P4**: Aplicar compresión sin pérdidas con predicción y Rice
5. **P5**: Usar transformadas (DCT) para compresión y filtrado

## 📊 Conceptos Clave

### Codificación PCM
- **Cuantización uniforme**: División del rango de valores en niveles iguales
- **Resolución**: Número de bits por muestra (R) determina la calidad
- **Error de cuantización**: Diferencia entre señal original y cuantizada

### Codificación Rice
- **Código unario**: Representación de enteros no negativos con n ceros + 1
- **Predicción**: Uso de valores anteriores para reducir redundancia
- **Compresión sin pérdidas**: Reconstrucción perfecta de la señal original

### Transformada DCT
- **Compactación**: Concentración de energía en pocos coeficientes
- **Ganancia de compactación**: Medida de eficiencia de la transformada
- **Filtrado**: Eliminación de coeficientes de alta frecuencia

## 📝 Notas Importantes

- Los archivos PDF (`l1.pdf` a `l5.pdf`) contienen los enunciados detallados de cada práctica
- Los archivos en `data/` son necesarios para ejecutar los ejemplos
- Los archivos `.bin` generados contienen datos codificados en formato binario
- Las funciones están diseñadas para ser compatibles con MATLAB cuando es posible
- El formato de almacenamiento por columnas (column-major) se mantiene para compatibilidad

## 🎯 Objetivos de Aprendizaje

Este proyecto cubre:

1. **Procesamiento de audio**: Lectura, reproducción y análisis de señales
2. **Codificación de imágenes**: Conversión entre formatos y almacenamiento binario
3. **Cuantización**: PCM y efectos de la resolución en la calidad
4. **Compresión sin pérdidas**: Técnicas de predicción y codificación entrópica
5. **Transformadas**: DCT y su aplicación en compresión y filtrado
6. **Análisis de señales**: Cálculo de métricas (SNR, MSE, ganancia)

## 🔬 Métricas y Análisis

### Métricas Implementadas

- **MSE (Mean Squared Error)**: Error cuadrático medio entre señales
- **SNR (Signal-to-Noise Ratio)**: Relación señal-ruido en dB
- **Ganancia de compactación**: Eficiencia de la transformada DCT
- **Tasa de compresión**: Relación entre tamaños de archivo original y comprimido

## 📄 Licencia

Este es un proyecto académico para fines educativos.

## 👤 Autor

Proyecto desarrollado como parte del curso de Procesamiento Digital de Señales y Comunicaciones.

---

**Nota**: Asegúrate de tener todos los archivos de datos en el directorio `data/` antes de ejecutar las prácticas. Algunos scripts pueden requerir ajustes de rutas según tu configuración.

