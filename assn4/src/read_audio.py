#!/usr/bin/env python
import wave
import struct
import os
import sys

# gets tuple of ("-f|-d", [path]) and determines if it's a dir
def is_directory(audio_input):
    return audio_input[0] == "-d"

def is_mp3(file):
    return True

"""
create_file_array:
Creates an array of all valid files from input
If it's a single file, creates a single-element array
If it's a directory, creates an array with its valid files, 
filters out files with unsupported formats
Assumes that audio_input is a valid path to something that exists

INPUT: Valid paths to a file or directory
OUTPUT: Array of all valid files from input
"""
def create_file_array(audio_input):
    if (is_directory(audio_input)):
        input_dir = os.listdir(audio_input[1])
        file_array = []
        for filename in input_dir:
            full_filename = audio_input[1] + '/' + filename
            if (validate_file(full_filename)):
                file_array.append(full_filename)
            else:
                print "Program terminating..."
                sys.exit(2)
        return file_array
    else:
        return [audio_input[1]]

def validate_file(file_input):
    try:
        wave.open(file_input, 'rb')
        return True
    except IOError:
        print "ERROR: file ", file_input," does not exist"
    except wave.Error:
        print "ERROR: file ", file_input," is not a supported format"
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
        print "ERROR: directory ", path," does not exist"
    return False

def length(wave_file):
    wr = wave.open(wave_file, "rb")
    sample_rate = wr.getframerate()
    num_frames = wr.getnframes()
    wr.close()

    return num_frames / float(sample_rate);
