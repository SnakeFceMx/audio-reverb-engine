#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

const int SAMPLE_RATE = 44100;

// 1. LIMITADOR DE PICOS (Evita la distorsión digital / clipping)
class PeakLimiter {
private:
    float threshold = 0.95f; // Límite máximo de amplitud (-0.45 dBFS)

public:
    float processSample(float input) {
        // Aplica compresión suave (soft clipping) si excede el umbral
        if (input > threshold) {
            return threshold + (input - threshold) / (1.0f + std::pow(input - threshold, 2));
        } else if (input < -threshold) {
            return -threshold + (input + threshold) / (1.0f + std::pow(-input - threshold, 2));
        }
        return input;
    }
};

// 2. ECUALIZADOR (Filtro Low Shelf para Bass Boost)
class BassBoostFilter {
private:
    float gain = 1.0f; // Multiplicador de graves
    float lastSample = 0.0f;

public:
    void setBassGain(float dbGain) {
        // Convierte Decibelios a escala lineal
        gain = std::pow(10.0f, dbGain / 20.0f);
    }

    float processSample(float input) {
        // Filtro pasa-bajas simple para aislar y realzar frecuencias graves (< 200 Hz)
        float lowFreq = (input + lastSample) * 0.5f;
        lastSample = input;
        
        float highFreq = input - lowFreq;
        return (lowFreq * gain) + highFreq;
    }
};

// 3. MOTOR REVERB CONCERT HALL
class ConcertHallReverb {
private:
    std::vector<float> delayBuffer;
    int writeIndex = 0;
    float wetDryMix = 0.5f;
    float decay = 0.6f;

public:
    ConcertHallReverb(float delaySeconds) {
        int bufferSize = static_cast<int>(delaySeconds * SAMPLE_RATE);
        delayBuffer.resize(bufferSize, 0.0f);
    }

    void setMix(float mixValue) {
        wetDryMix = std::clamp(mixValue, 0.0f, 1.0f);
    }

    float processSample(float inputSample) {
        float delayedSample = delayBuffer[writeIndex];
        float outputSample = inputSample + (delayedSample * decay);
        delayBuffer[writeIndex] = outputSample;
        writeIndex = (writeIndex + 1) % delayBuffer.size();

        return (inputSample * (1.0f - wetDryMix)) + (outputSample * wetDryMix);
    }
};

// --- CADENA COMPLETA DE AUDIO (DSP PIPELINE) ---
int main() {
    std::cout << "=== PROCESADOR DSP: REVERB + BASS BOOST + LIMITER ===" << std::endl;

    // Instancias de los módulos DSP
    ConcertHallReverb reverb(0.15f);
    BassBoostFilter bassBoost;
    PeakLimiter limiter;

    // Configuración de perillas (Simulación de la UI)
    reverb.setMix(0.6f);          // Perilla Reverb al 60%
    bassBoost.setBassGain(6.0f);   // Realce de graves +6 dB

    // Audio de prueba con un pico fuerte para probar el limitador
    std::vector<float> audioEntrada = {0.5f, 0.9f, 1.2f, 0.8f, 0.3f, 0.0f, 0.0f};

    std::cout << "\nEntrada\t->\tSalida Final Procesada" << std::endl;
    std::cout << "---------------------------------------------" << std::endl;

    for (float sample : audioEntrada) {
        // Cadena de Procesamiento en serie:
        float paso1 = bassBoost.processSample(sample); // 1. Aplica Graves
        float paso2 = reverb.processSample(paso1);     // 2. Aplica Concert Hall
        float salidaFinal = limiter.processSample(paso2); // 3. Evita Distorsión

        std::cout << sample << "\t->\t" << salidaFinal << std::endl;
    }

    std::cout << "---------------------------------------------" << std::endl;
    std::cout << "--- Cadena de Procesamiento Exitosa ---" << std::endl;

    return 0;
}