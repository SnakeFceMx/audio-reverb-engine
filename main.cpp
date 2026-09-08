#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

const int SAMPLE_RATE = 44100;

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

// Instancia global del motor
ConcertHallReverb g_reverb(0.15f);

// Funciones expuestas hacia la interfaz gráfica (UI)
extern "C" {
    void set_reverb_mix(float mix) {
        g_reverb.setMix(mix);
    }

    float process_audio_sample(float sample) {
        return g_reverb.processSample(sample);
    }
}