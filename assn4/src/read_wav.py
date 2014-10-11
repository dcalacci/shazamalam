#!/usr/bin/env python
import wave
import struct

def validate_file(file_input):
    try:
        wave.open(file_input, 'rb')
        return True
    except IOError:
        print "ERROR: ", file_input," does not exist"
    except wave.Error:
        print "ERROR: ", file_input," is not a supported format"
    return False

def length(wave_file):
    wr = wave.open(wave_file, "rb")
    sample_rate = wr.getframerate()
    num_frames = wr.getnframes()
    wr.close()

    return num_frames / float(sample_rate);
