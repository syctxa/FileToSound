import wave, struct, math, random, array

def gen_sine_list(freq, nframes, frate):
    sine_list = []
    for x in range(nframes):
        sine_list.append(math.sin(2.0*math.pi*freq*(x/frate)))
    
    return sine_list

sampleRate = 44100 # hertz
duration = 1 # seconds
frequency = 103.0 # hertz
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setframerate(sampleRate)
data = array.array('h')
for s in gen_sine_list(frequency, int (duration * sampleRate), sampleRate):
   data.append(int(s*5/2))
print(data)
obj.writeframesraw( data )
obj.close()