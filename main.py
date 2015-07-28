import sys
import time
from pyo import *

from dna_to_music import nucleotide_to_hz
from seq_reading import sequences_in_file
# Useful pyo example lines

# Randomly choose from a list.
# rnd = Choice(choice=freqs, freq=[3,4])
# Call after a time
# a = CallAfter(callback, 2, [300,301])
# Call repeatedly after intervals
# p = Pattern(callback, .125)

# Convert midi not to frequency
# freqs = midiToHz([60,62,64,65,67,69,71,72])

SERVER = None

seq = sequences_in_file("assets/sequences/kampy_full.fasta").next()


def play_music():
    wave = SineLoop(1000, feedback=0.05, mul=.2).out()
    def each_note():
        nucleo = seq.next()
        wave.freq = nucleotide_to_hz(nucleo)

    p = Pattern(each_note, 1.0/16)
    p.play()

    time.sleep(100*10)



def main():
    global SERVER
    SERVER = Server().boot()
    SERVER.start()

    play_music()

    SERVER.stop()
    SERVER.shutdown()
    sys.exit(0)


if __name__ == "__main__":
    main()
