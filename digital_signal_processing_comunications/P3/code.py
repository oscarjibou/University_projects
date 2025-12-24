def codPCM(x, R, fi):

    N = x.size  # Número de muestras
    Delta = 2.0 ** (1 - R)  # = 2^(1-R) Paso de cuantización

    k_index = np.floor(x / Delta)
    k_index = k_index.astype(np.int32)
    offset = 2 ** (R - 1)
    kprime = k_index + offset

    kprime_uint16 = kprime.astype(np.uint16)

    with open(fi, "wb") as f:

        f.write(struct.pack("B", R))
        f.write(struct.pack("<I", N))
        f.write(kprime_uint16.tobytes())


def decPCM(fi):
    with open(fi, "rb") as f:

        R_data = f.read(1)
        R = struct.unpack("B", R_data)[0]

        N_data = f.read(4)
        N = struct.unpack("<I", N_data)[0]

        kprime_data = f.read(2 * N)
        kprime_arr = np.frombuffer(kprime_data, dtype=np.uint16)

    offset = 2 ** (R - 1)
    k_arr = kprime_arr.astype(np.int32) - offset
    Delta = 2.0 ** (1 - R)
    y = k_arr.astype(np.float64) * Delta

    return y, R


def ejemplo_PCM():
    # 1) Leer vt1.wav
    x, fs = sf.read("../data/vt1.wav")  # x ~ señal en [-1,1]
    print(f"Leídos {len(x)} samples, fs={fs} Hz")

    # 2) Elegir R ( R es el número de bits por muestra)
    R = 13
    # 3) Codificar
    codPCM(x, R, "vt1_pcm.bin")

    # 4) Decodificar
    y, R_leido = decPCM("vt1_pcm.bin")

    # 5) Calcular error RMS o MSE
    mse = np.mean((x - y) ** 2)
    print(f"Error cuadrático medio (MSE) = {mse:.6e}")

    # 6) Reproducir original
    print("Reproduciendo señal original...")
    sd.play(x, fs)
    sd.wait()

    # 7) Reproducir señal decodificada
    print("Reproduciendo señal decodificada...")
    sd.play(y, fs)
    sd.wait()

    # Observa si hay diferencia audible
    print("Fin del ejemplo.")


ejemplo_PCM()
