import ctypes
import tkinter as tk
from tkinter import ttk

# 1. Cargar el motor DSP compilado
lib = ctypes.CDLL('./libreverb.so')
lib.set_reverb_mix.argtypes = [ctypes.c_float]

# 2. Funciones para actualizar la perilla
def actualizar_reverb(val):
    porcentaje = float(val)
    mix_factor = porcentaje / 100.0
    lib.set_reverb_mix(mix_factor)
    lbl_valor.config(text=f"{int(porcentaje)}%")

# 3. Crear la ventana principal
root = tk.Tk()
root.title("Concert Hall Reverb Control")
root.geometry("350x250")
root.configure(bg="#1e1e2e")

# Estilos de texto
titulo = tk.Label(root, text="MOTOR DSP REVERB", font=("Helvetica", 14, "bold"), fg="#cdd6f4", bg="#1e1e2e")
titulo.pack(pady=15)

lbl_instruccion = tk.Label(root, text="Ajusta el efecto Concert Hall:", font=("Helvetica", 10), fg="#a6adc8", bg="#1e1e2e")
lbl_instruccion.pack(pady=5)

# Control deslizable (Simulador de Perilla)
slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=actualizar_reverb)
slider.set(50)  # Valor inicial al 50%
slider.pack(pady=15, fill="x", px=30)

lbl_valor = tk.Label(root, text="50%", font=("Helvetica", 18, "bold"), fg="#89b4fa", bg="#1e1e2e")
lbl_valor.pack(pady=5)

root.mainloop()
