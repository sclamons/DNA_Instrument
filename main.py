from pyo import *
import time
s = Server().boot()
f = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=5, mul=.5)
a = Sine(440, 0, mul=1).out()
s.start()
f.play()
time.sleep(4)

s.stop()
