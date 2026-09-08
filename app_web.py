import streamlit as st
import ctypes

# 1. Cargar el motor C++
lib = ctypes.CDLL('./libreverb.so')
lib.set_reverb_mix.argtypes = [ctypes.c_float]
lib.process_audio_sample.argtypes = [ctypes.c_float]
lib.process_audio_sample.restype = ctypes.c_float

st.title("🎛️ Concert Hall Reverb Engine")
st.write("Controla el motor DSP en C++ en tiempo real desde la nube.")

# 2. Control de Perilla / Slider
porcentaje = st.slider("Ajustar Reverb Mix (%)", min_value=0, max_value=100, value=50)

# Enviar valor al motor C++
mix_factor = porcentaje / 100.0
lib.set_reverb_mix(mix_factor)

st.success(f"Nivel de Reverb enviado a C++: {porcentaje}%")

# 3. Simulador de procesamiento en vivo
st.subheader("Simulación de Muestras DSP")
if st.button("Procesar Muestra de Prueba"):
    salida = lib.process_audio_sample(0.8)
    st.info(f"Entrada: 0.8  -->  Salida Procesada C++: {salida:.4f}")
