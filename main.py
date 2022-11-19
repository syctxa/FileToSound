
from utils.ToneGen2 import *
import wave
import array
import random

test_str = open("test.py", "r").read()
print("The original string is : " + str(test_str))
data = []

for chr in test_str:
    data.append(int('{:04X}'.format(ord(chr)), 16))
print("The unicode converted String : " + str(data))

generator = ToneGeneratorV2()

amplitude = 5
step_duration = 0.02

'''for frequency in data:
    print("Playing tone at {0:0.2f} Hz".format(frequency))
    sf = generator.play(frequency, step_duration, amplitude)
    while generator.is_playing():
        pass'''
filename = str(data[0]) + str(random.randint(10000, 99999)) + '.wav'
amplitude = 64000     # multiplier for amplitude (max is 65,520 for 16 bit)

nframes = int (step_duration*len(data)*(44100/4))

sine_list = gen_sine_list(data, 44100, nframes)
gen_wav(filename, sine_list, data, 44100, amplitude, nframes)

print("File {} was saved".format(filename)) 