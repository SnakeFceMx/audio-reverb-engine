import ctypes
import numpy as np
import wave

# 1. Cargar la librería C++
lib = ctypes.CDLL('./libreverb.so')
lib.set_reverb_mix.argtypes = [ctypes.c_float]
lib.process_audio_sample.argtypes = [ctypes.c_float]
lib.process_audio_sample.restype = ctypes.c_float

# 2. Generar un tono de audio de prueba (44100 Hz, 2 segundos)
sample_rate = 44100
duracion = 2.0
t = np.linspace(0, duracion, int(sample_rate * duracion), False)
# Nota musical (A4 - 440Hz)
audio_original = (np.sin(2 * np.pi * 440 * t) * 0.5).astype(np.float32)

# 3. Aplicar Reverb al 70% usando nuestro motor C++
lib.set_reverb_mix(0.7)
audio_procesado = np.zeros_like(audio_original)

for i in range(len(audio_original)):
    audio_procesado[i] = lib.process_audio_sample(audio_original[i])

# 4. Guardar el resultado en un archivo .wav escuchable
audio_int16 = (audio_procesado * 32767).astype(np.int16)
with wave.open('salida_concert_hall.wav', 'w') as f:
    f.setnchannels(1)     # Mono
    f.setsampwidth(2)      # 16-bit
    f.setframerate(sample_rate)
    f.writeframes(audio_int16.tobytes())

print("¡Audio procesado con éxito! Se ha generado 'salida_concert_hall.wav'")
