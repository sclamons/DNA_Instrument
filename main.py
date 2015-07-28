import time
from pyo import *

scale = midiToHz([60,62,64,65,67,69,71,72])

def play_music(server):
    freqs = midiToHz([60,62,64,65,67,69,71,72])
    rnd = Choice(choice=freqs, freq=[3,4])
    a = SineLoop(rnd, feedback=0.05, mul=.2).out()

    time.sleep(100.000000)


def main():
    s = Server().boot()
    s.start()

    play_music(s)

    s.stop()


if __name__ == "__main__":
    main()
