#!/usr/bin/env python
import wave
import struct
import os

# gets tuple of ("-f|-d", [path]) and determines if it's a dir
def is_directory(audio):
    return audio[0] == "-d"

def validate_file(file_input):
    path = file_input[1]
    try:
        if (is_directory(file_input)):
            os.listdir(path)
        else:
            wave.open(path, 'rb')
        return True
    except IOError:
        print "ERROR: ", path," does not exist"
    except OSError:
        print "ERROR: ", path," does not exist"
    except wave.Error:
        print "ERROR: ", path," is not a supported format"
    return False

def length(wave_file):
    wr = wave.open(wave_file, "rb")
    sample_rate = wr.getframerate()
    num_frames = wr.getnframes()
    wr.close()

    return num_frames / float(sample_rate);
