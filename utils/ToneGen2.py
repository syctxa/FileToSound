'''
tonegen: generate tones based on frequency in Hz provided
'''
import argparse
import math
import struct
import wave
import sys
import numpy
import pyaudio

#-------------------------------------------------------------------------------
# generate sine_list
#-------------------------------------------------------------------------------
def gen_sine_list(freqs, frate, nframes):
    sine_list = []
    for freq in freqs:
        for x in range(nframes):
            sine_list.append(math.sin(2.0*math.pi*int(freq)*(x/int(frate))))
    
    return sine_list

#-------------------------------------------------------------------------------
# save tone to wav file
#-------------------------------------------------------------------------------
def gen_wav(fname, sine_list, freq, frate, amp, nframes):
    nchannels = 1
    sampwidth = 2
    comptype = "NONE"
    compname = "not compressed"

    wav_file = wave.open(fname, "w")
    wav_file.setparams((nchannels, sampwidth, int(frate), nframes,
        comptype, compname))

    for s in sine_list:
        # write the audio frames to file
        wav_file.writeframes(struct.pack('h', int(s*amp)))

    wav_file.close()

    return

#-------------------------------------------------------------------------------
# get arguments
#-------------------------------------------------------------------------------
def get_args():
    parser = argparse.ArgumentParser(
        description='Wave file generator')

    parser.add_argument(
        '-f', '--frequency', \
                help='Set frequency, in Hz', required=False, default=None)
    parser.add_argument(
        '-r', '--framerate', \
                help='Set frame rate of audio file, in frames per second', \
                required=False, default = None)
    parser.add_argument(
        '-t', '--time', \
                help='Set duration of the sound, in seconds', \
                required=False, default=None)

    args = parser.parse_args()

    if (len(sys.argv) == 1):
        print('tonegenGUI -f <frequency> -r <framerate> -t <time> -g')
        print('    f: frequency (Hz), Eg. 440')
        print('    r: frame rate (frames/samples per second), E.g. 41000')
        print('    t: audio length (seconds), E.g. 5')
        print('    g: display dialog box to enter values')
        exit()

    return args

#-------------------------------------------------------------------------------
# get audio parameters
#-------------------------------------------------------------------------------
def get_params(args, params):
    if (args.frequency != None):
        params['Frequency'] = args.frequency
    if (args.framerate != None):
         params['Framerate'] = args.framerate
    if (args.time != None):
         params['Time'] = args.time

    return params

#-------------------------------------------------------------------------------
# main
#-------------------------------------------------------------------------------
def main():

    # sample run: tonegen -f 440 -r 44100 -t 5 -g
    #   f: frequency (Hz)
    #   r: frame rate (frames/samples per second)
    #   t: audio length (seconds)
    #   g: flag for GUI

    params = {'Frequency': '', 'Framerate': '', 'Time': ''}

    print("")
    print("======================================")
    print("Tone Generator")
    print("")

    args = get_args()   # get command line arguments

    params = get_params(args, params)   # get parameters from dialgo box (GUI)

    print("Frequency: {}".format(params['Frequency']))
    print("Framerate: {}".format(params['Framerate']))
    print("Time:      {}".format(params['Time']))
    print("")
    if (params['Frequency'] != '' and params['Framerate'] != '' and params['Time'] != ''):
        filename = str(params['Frequency']) + 'Hz_' + str(params['Time']) + 's.wav'
        amplitude = 64000     # multiplier for amplitude (max is 65,520 for 16 bit)

        nframes = int (int(params['Time']) * int(params['Framerate']))

        sine_list = gen_sine_list([params['Frequency']], params['Framerate'], nframes)
        gen_wav(filename, sine_list, params['Frequency'], params['Framerate'], amplitude, nframes)

        print("File {} was saved".format(filename)) 
    else:
        print("Some values are not valid")
    print("======================================")
class ToneGeneratorV2:
    def __init__(self, samplerate=44100, frames_per_buffer=4410):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False

    def sinewave(self):
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            # We don't need a full buffer or audio so pad the end with 0's
            xs = numpy.arange(self.buffer_offset,
                              self.x_max)
            tmp = self.amplitude * numpy.sin(xs * self.omega)
            out = numpy.append(tmp,
                               numpy.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = numpy.arange(self.buffer_offset,
                              self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * numpy.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer
        return out
    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(numpy.float32)
            return (data.tostring(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)
 
    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False
 
    def play(self, frequency, duration, amplitude):
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)
        return self
if __name__ == "__main__":
    main()
