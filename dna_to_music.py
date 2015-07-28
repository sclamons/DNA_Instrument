from pyo import midiToHz
from nucleotides import A, C, T, G, N

nucleotide_midi = {
    A: 80,
    T: 82,
    G: 60,
    C: 65,
    N: 75
}

def nucleotide_to_hz(nucleo):
    print nucleo
    # first make it a midi.  This is cute
    midi_value = nucleotide_midi[nucleo]
    return midiToHz(midi_value)
