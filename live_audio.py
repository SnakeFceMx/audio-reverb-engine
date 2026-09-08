import ctypes
import numpy as np
import time

# 1. Cargar el motor DSP C++
lib = ctypes.CDLL('./libreverb.so')
lib.set_reverb_mix.argtypes = [ctypes.c_float]
lib.process_audio_sample.argtypes = [ctypes.c_float]
lib.process_audio_sample.restype = ctypes.c_float

# Ajustar Reverb Mix al 70%
lib.set_reverb_mix(0.7)

print("🎛️ SIMULADOR DE STREAMING EN TIEMPO REAL (MODO NUBE)")
print("Procesando bloques de 1024 muestras en tiempo real mediante el motor C++...\n")

blocksize = 1024
samplerate = 44100

# 2. Bucle que simula la llegada constante de audio de YouTube/Sistema
try:
    bloque_num = 1
    while True:
        # Generar un bloque de 1024 muestras (Simulación de audio en vivo)
        t = np.linspace(0, blocksize / samplerate, blocksize, endpoint=False)
        indata = np.sin(2 * np.pi * 440 * t) # Tono de prueba
        outdata = np.zeros_like(indata)

        # Procesar bloque en C++
        for i in range(blocksize):
            outdata[i] = lib.process_audio_sample(indata[i])

        print(f"-> Bloque #{bloque_num} procesado en C++ | Muestra entrada: {indata[0]:.3f} | Muestra Reverb: {outdata[0]:.3f}")
        bloque_num += 1
        
        # Simular el intervalo del buffer real (~23ms por bloque)
        time.sleep(blocksize / samplerate)

except KeyboardInterrupt:
    print("\nTransmisión simulada detenida.")
