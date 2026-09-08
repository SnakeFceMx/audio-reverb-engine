import ctypes

# Cargar la librería C++
lib = ctypes.CDLL('./libreverb.so')

lib.set_reverb_mix.argtypes = [ctypes.c_float]
lib.process_audio_sample.argtypes = [ctypes.c_float]
lib.process_audio_sample.restype = ctypes.c_float

print("=== INTERFAZ VIRTUAL: CONTROL DE PERILLA CONCERT HALL ===")
print("Gira la perilla de 0 a 100% para escuchar la resonancia de la sala.")
print("Escribe 'salir' para terminar.\n")

while True:
    val = input("Girar Perilla Reverb (0 - 100%): ")
    if val.lower() == 'salir':
        break
    
    try:
        porcentaje = float(val)
        if 0 <= porcentaje <= 100:
            mix_factor = porcentaje / 100.0
            
            # 1. Enviar valor de la perilla al motor C++
            lib.set_reverb_mix(mix_factor)
            
            # 2. Simular un flujo continuo de 5 muestras para llenar la sala de sonido
            muestras_entrada = [0.8, 0.6, 0.4, 0.2, 0.0]
            print(f"\n --- Procesando audio con la Perilla al {porcentaje}% ---")
            
            for i, muestra in enumerate(muestras_entrada):
                salida = lib.process_audio_sample(muestra)
                print(f" Muestra {i+1} | Entrada: {muestra:.1f} -> Salida Procesada: {salida:.4f}")
            print(" -----------------------------------------------------\n")
        else:
            print("Por favor introduce un número entre 0 y 100.\n")
    except ValueError:
        print("Entrada no válida.\n")