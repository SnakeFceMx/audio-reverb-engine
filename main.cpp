#include <iostream>
#include <vector>
#include <cmath>

// Configuración básica de audio
const int SAMPLE_RATE = 44100; // Calidad de audio estándar (44.1 kHz)

// Clase principal del motor Reverb (Efecto Concert Hall)
class ConcertHallReverb {
private:
    std::vector<float> delayBuffer;
    int writeIndex = 0;
    float wetDryMix = 0.5f; // Perilla: 0.0 (Sin Reverb) a 1.0 (100% Concert Hall)
    float decay = 0.6f;      // Eco y resonancia de la sala

public:
    ConcertHallReverb(float delaySeconds) {
        int bufferSize = static_cast<int>(delaySeconds * SAMPLE_RATE);
        delayBuffer.resize(bufferSize, 0.0f);
    }

    // Ajuste en tiempo real (Equivalente a girar la perilla en la app)
    void setMix(float mixValue) {
        if (mixValue < 0.0f) mixValue = 0.0f;
        if (mixValue > 1.0f) mixValue = 1.0f;
        wetDryMix = mixValue;
    }

    // Procesamiento sample por sample (DSP en tiempo real)
    float processSample(float inputSample) {
        float delayedSample = delayBuffer[writeIndex];
        
        // Algoritmo de realimentación para simular las paredes de una sala de conciertos
        float outputSample = inputSample + (delayedSample * decay);
        delayBuffer[writeIndex] = outputSample;

        writeIndex = (writeIndex + 1) % delayBuffer.size();

        // Mezcla final: Sonido Original (Dry) + Sonido Procesado (Wet)
        return (inputSample * (1.0f - wetDryMix)) + (outputSample * wetDryMix);
    }
};

int main() {
    std::cout << "--- Generando Rafaga de Audio en Tiempo Real ---" << std::endl;
    
    ConcertHallReverb concertHall(0.15f);
    concertHall.setMix(0.7f); // Perilla al 70%

    // Simulamos 10 muestras continuas de sonido
    std::vector<float> audioEntrada = {0.8f, 0.5f, 0.2f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f};

    std::cout << "\nEntrada\t->\tSalida Procesada (Con Reverb/Eco)" << std::endl;
    std::cout << "---------------------------------------------" << std::endl;

    for (size_t i = 0; i < audioEntrada.size(); ++i) {
        float salida = concertHall.processSample(audioEntrada[i]);
        std::cout << audioEntrada[i] << "\t->\t" << salida << std::endl;
    }

    std::cout << "---------------------------------------------" << std::endl;
    std::cout << "--- Resonancia de la Sala Simulada con Exito ---" << std::endl;

    return 0;
}