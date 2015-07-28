import sys
import time

from pyo import *

# Useful pyo example lines

# Randomly choose from a list.
# rnd = Choice(choice=freqs, freq=[3,4])
# Call after a time
# a = CallAfter(callback, 2, [300,301])
# Call repeatedly after intervals
# p = Pattern(callback, .125)

SERVER = None

def play_music():
    freqs = midiToHz([60,62,64,65,67,69,71,72])


    wave = SineLoop(100, feedback=0.05, mul=.2).out()
    def each_note():
        wave.freq = freqs.pop(0)
        freqs.append(wave.freq)

    p = Pattern(each_note, .125)
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
