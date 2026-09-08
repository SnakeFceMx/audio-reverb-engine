import ctypes
import numpy as np
import sounddevice as sd
import time

# 1. Cargar el motor DSP C++
lib = ctypes.CDLL('./libreverb.so')
lib.set_reverb_mix.argtypes = [ctypes.c_float]
lib.process_audio_sample.argtypes = [ctypes.c_float]
lib.process_audio_sample.restype = ctypes.c_float

# Fijar nivel de Reverb al 60%
lib.set_reverb_mix(0.6)

# 2. Función Callback: Se ejecuta automáticamente cada vez que la tarjeta de sonido tiene nuevos datos
def audio_callback(indata, outdata, frames, time_info, status):
    if status:
        print(status)
    
    # indata contiene el audio en vivo que entra (micrófono / cable virtual)
    # Procesamos muestra por muestra en C++
    for i in range(frames):
        muestra_entrada = indata[i, 0] # Canal 1 (Mono)
        muestra_procesada = lib.process_audio_sample(muestra_entrada)
        outdata[i, 0] = muestra_procesada # Salida a los altavoces

print("🎛️ Motor DSP C++ escuchando entrada de audio en tiempo real...")
print("Presiona Ctrl+C para detener.")

# 3. Abrir Stream de Audio (Entrada -> Procesamiento C++ -> Salida)
try:
    with sd.Stream(channels=1, callback=audio_callback, samplerate=44100, blocksize=1024):
        while True:
            time.sleep(0.1)
except KeyboardInterrupt:
    print("\nTransmisión en tiempo real detenida.")
