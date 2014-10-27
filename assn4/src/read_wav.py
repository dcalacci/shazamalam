#!/usr/bin/env python
import wave
import struct
import os

# gets tuple of ("-f|-d", [path]) and determines if it's a dir
def is_directory(audio_input):
    return audio_input[0] == "-d"

def create_file_array(audio_input):
    if (is_directory(audio_input)):
        dir_path = audio_input[1]
        input_dir = os.listdir(dir_path)
        return [(dir_path + '/' + filename) for filename in input_dir]
    else:
        return [audio_input[1]]

def validate_file(file_input):
    try:
        wave.open(file_input, 'rb')
        return True
    except IOError:
        print "ERROR: ", file_input," does not exist"
    except wave.Error:
        print "ERROR: ", file_input," is not a supported format"
    return False


def validate_input(file_input):
    path = file_input[1]
    try:
        if (is_directory(file_input)):
            os.listdir(path)
            return True
        else:
            return validate_file(path)
    except OSError:
        print "ERROR: ", path," does not exist"
    return False

def length(wave_file):
    wr = wave.open(wave_file, "rb")
    sample_rate = wr.getframerate()
    num_frames = wr.getnframes()
    wr.close()

    return num_frames / float(sample_rate);
