import streamlit as st
import ctypes
import numpy as np
import os
from pydub import AudioSegment
import io

st.set_page_config(page_title="Concert Hall Reverb DSP", page_icon="🎛️", layout="centered")

# 1. Cargar el motor DSP C++
@st.cache_resource
def load_dsp_library():
    so_path = os.path.abspath("./libreverb.so")
    if os.path.exists(so_path):
        lib = ctypes.CDLL(so_path)
        lib.set_reverb_mix.argtypes = [ctypes.c_float]
        lib.process_audio_sample.argtypes = [ctypes.c_float]
        lib.process_audio_sample.restype = ctypes.c_float
        return lib
    return None

lib = load_dsp_library()

st.title("🎛️ Concert Hall Reverb Engine")
st.caption("Procesador de Audio en C++ compatible con archivos MP3 y WAV")

if lib is None:
    st.error("❌ No se encontró la librería 'libreverb.so'. Asegúrate de compilar main.cpp.")
    st.stop()

# 2. Control de Reverb
reverb_mix = st.slider("Nivel de Reverb Mix (%)", min_value=0, max_value=100, value=60, step=5)
lib.set_reverb_mix(reverb_mix / 100.0)

# 3. Cargar archivo MP3 o WAV
uploaded_file = st.file_uploader("Selecciona un archivo de audio (MP3 o WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format=uploaded_file.type)
    
    if st.button("⚡ Procesar Audio con Motor DSP C++"):
        with st.spinner("Decodificando y aplicando filtro Reverb en C++..."):
            file_bytes = uploaded_file.read()
            
            # Cargar con PyDub (Soporta MP3 y WAV)
            file_ext = uploaded_file.name.split('.')[-1].lower()
            audio_segment = AudioSegment.from_file(io.BytesIO(file_bytes), format=file_ext)
            
            # Convertir a Mono y extraer muestras float32
            audio_segment = audio_segment.set_channels(1)
            sample_rate = audio_segment.frame_rate
            samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
            
            # Normalizar a rango [-1.0, 1.0]
            max_val = np.max(np.abs(samples)) if np.max(np.abs(samples)) > 0 else 1.0
            samples_norm = samples / max_val
            
            # Procesar muestra por muestra en C++
            processed_samples = np.zeros_like(samples_norm)
            for i in range(len(samples_norm)):
                processed_samples[i] = lib.process_audio_sample(samples_norm[i])
            
            # Convertir de vuelta a enteros de 16-bits
            processed_samples_int16 = np.int16(processed_samples * 32767)
            
            # Recrear AudioSegment procesado
            processed_segment = AudioSegment(
                processed_samples_int16.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=1
            )
            
            # Exportar a MP3 en memoria
            output_buffer = io.BytesIO()
            processed_segment.export(output_buffer, format="mp3", bitrate="192k")
            output_bytes = output_buffer.getvalue()
            
            st.success("¡Audio procesado con éxito!")
            st.audio(output_bytes, format="audio/mp3")
            
            st.download_button(
                label="📥 Descargar Audio Procesado (MP3)",
                data=output_bytes,
                file_name=f"procesado_{uploaded_file.name}.mp3",
                mime="audio/mp3"
            )
