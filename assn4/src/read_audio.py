#!/usr/bin/env python
import wave
import struct
import os
import sys
import subprocess

# gets tuple of ("-f|-d", [path]) and determines if it's a dir
def is_directory(audio_input):
    return audio_input[0] == "-d"

"""
is_mp3:
Given a file path, determine if the file is not only an mp3,
but one with the right specifications. 

INPUT: A file path (at the stage is_mp3 is called, we know
that the file is a valid file that exists so we dont check for it)
OUTPUT: True if and only if the file path isL
    - a valid mp3 file
    - is MPEG
    - is Layer III
    - is the right version : v1 in the header (?) 
"""
def is_mp3(file):
    #first, check the end of the file path
    if(file[-4:] != ".mp3"):
        return False

    #then, check that its the right format
    file_header = subprocess.check_output(["file", file])
    format_string = "MPEG"
    layer_string = "layer III"
    version_string = "v1"
    if format_string not in file_header or layer_string not in file_header: #currently does not include version
        return False

    #otherwise
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
        if is_mp3(file_input):
            return True

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


def create_temp_wav_file(file_path):
    path_array = file_path.split('/')
    filename = path_array[-1]

    new_wav_file_path = '/tmp/'+ filename.split('.')[0] + '.wav'

    os.system('/course/cs4500f14/bin/lame -V2 --silent --decode ' + file_path + ' ' + new_wav_file_path)

    return new_wav_file_path

def delete_temp_file(file_path):

    if '/tmp' in file_path:
        os.system('rm -f ' + file_path)





