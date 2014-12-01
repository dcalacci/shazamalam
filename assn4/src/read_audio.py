#!/usr/bin/env python
from scipy.io import wavfile
from scipy.signal import resample
from os.path import basename
import numpy as np
import wave
import os
import sys
import subprocess
import re

#LAME_CMD = ['/usr/bin/env', 'lame']
LAME_CMD = ['/course/cs4500f14/bin/lame']

OGGDEC_CMD = ['/usr/bin/env', 'oggdec']

RESAMPLE_RATE = 44100


def get_mono(fpath):
    """ Converts the given wav file to 5512 PCM Mono.
    """
    if is_mp3(fpath):
        fpath = create_temp_wav_file_from_mp3(fpath)
    elif is_ogg(fpath):
        fpath = create_temp_wav_file_from_ogg(fpath)
    samplerate, channels = wavfile.read(fpath)

    delete_temp_file(fpath)

    # if the sample rate isn't already 44100, resample the file
    if samplerate != RESAMPLE_RATE:
        channels = resample_pcm(samplerate, channels)

    # if it's mono, don't average them
    if type(channels[0]) != np.ndarray:
        return channels

    return np.mean(channels, axis=1).astype(int)


def resample_pcm(samplerate, channels, resample_rate=RESAMPLE_RATE):
    """Resamples the given PCM stream to resample_rate.
    """
    new_length = resample_rate * (len(channels) / samplerate)
    # convert to int so we have more exact matches
    return resample(channels, new_length).astype(int)


# gets tuple of ("-f|-d", [path]) and determines if it's a dir
def is_directory(audio_input):
    return audio_input[0] == "-d"


def is_mp3(file):
    """
    is_mp3:
    Given a file path, determine if the file is not only an mp3,
    but one with the right specifications.

    INPUT: A file path (at the stage is_mp3 is called, we know
    that the file is a valid file that exists so we dont check for it)
    OUTPUT: True if and only if the file path is:
        - a valid mp3 file
        - is MPEG
        - is Layer III
        - is the right version : v1 in the header (?)
    """
    # first, check the end of the file path
    if(file[-4:] != ".mp3"):
        return False

    # then, check that its the right format
    file_header = subprocess.check_output(["file", file])
    
    # our file may be a symbolic link, check for that
    # and reassign file header to the end of the link
    if "symbolic link" in file_header:
        file_header = re.split('[`\']', file_header)[1]
    
    format_string = "MPEG"
    layer_string = "layer III"
    version_string = "v1"
    # currently does not include version
    if format_string not in file_header or layer_string not in file_header:
        return False

    # otherwise
    return True


def is_ogg(file):
    """
    is_ogg:
    Given a file path, determine if the file is not only an ogg,
    but one with the right specifications.

    INPUT: A file path (at the stage is_ogg is called, we know
    that the file is a valid file that exists so we dont check for it)
    OUTPUT: True if and only if the file path is in a
    format that version 1.4.0 of the oggdec program will decode
    into a supported WAVE format without the use of any
    command-line options
    """
    # check the extension on the file
    if(file[-4:] != ".ogg"):
        return False

    # our file may be a symbolic link, check for that
    # and reassign file header to the end of the link
    if "symbolic link" in file_header:
        file_header = re.split('[`\']', file_header)[1]

    # check to make sure it's in the right format
    file_header = subprocess.check_output(["file", file])
    data_string = "Ogg data"
    
    if data_string not in file_header:
        return False

    return True


def create_file_array(audio_input):
    """
    create_file_array:
    Creates an array of all valid files from input
    If it's a single file, creates a single-element array
    If it's a directory, creates an array with its valid files,
    filters out files with unsupported formats
    Assumes that audio_input is a valid path to something that exists

    INPUT: Tuple containing valid path to a file or directory
    OUTPUT: Array of all valid files from input
    """
    if (is_directory(audio_input)):
        input_dir = os.listdir(audio_input[1])
        file_array = []
        for filename in input_dir:
            full_filename = audio_input[1] + '/' + filename
            if (validate_file(full_filename)):
                file_array.append(full_filename)
            else:
                sys.exit(2)
        return file_array
    else:
        return [audio_input[1]]


# INPUT: file path
# OUTPUT: Boolean
def validate_file(file_input):
    short_name = os.path.basename(file_input)
    try:
        wave.open(file_input, 'rb')
        return True
    except IOError:
        error = 'ERROR file ' + short_name + ' does not exist \n'
        sys.stderr.write(error)
    except wave.Error:
        if is_mp3(file_input):
            return True
        if is_ogg(file_input):
            return True

        error = 'ERROR file ' + short_name + ' is not a supported format \n'
        sys.stderr.write(error)
    return False


# INPUT: tuple (may be file or dir)
# OUTPUT: Boolean
def validate_input(audio_input):
    path = audio_input[1]
    short_name = os.path.basename(path)
    try:
        if (is_directory(audio_input)):
            os.listdir(path)
            return True
        else:
            return validate_file(path)
    except OSError:
        error = 'ERROR directory ' + short_name + ' does not exist \n'
        sys.stderr.write(error)
    return False


def create_temp_wav_file(file_path, cmd, args):
    """Creates a temporary wav file from the given file.

    Returns the full path of the temporary wav file.
    """
    new_wav_file_path = create_temp_wav_file_path(file_path)
    # output to /dev/null
    FNULL = open(os.devnull, 'w')
    res = subprocess.call(cmd + args,
                          stdout=FNULL,
                          stderr=subprocess.STDOUT)
    if res != 0:
        raise Exception("Call to " + str(cmd) + " failed. It's either not installed or it failed the conversion.")


def create_temp_wav_file_from_mp3(file_path):
    new_wav_file_path = create_temp_wav_file_path(file_path)
    args = ['-V2', '--silent', '--decode', file_path, new_wav_file_path]
    create_temp_wav_file(file_path, LAME_CMD, args)
    return new_wav_file_path


def create_temp_wav_file_from_ogg(file_path):
    new_wav_file_path = create_temp_wav_file_path(file_path)
    args = ['-o', new_wav_file_path, file_path]
    create_temp_wav_file(file_path, OGGDEC_CMD, args)
    return new_wav_file_path


TMP_FILE_DIR = '/scratch/dcalacci/'

def create_temp_wav_file_path(file_path):
    return os.path.join(TMP_FILE_DIR,  basename(file_path).split('.')[0] + '.wav')


def delete_temp_file(file_path):
    if TMP_FILE_DIR in file_path:
        os.system('rm -f ' + file_path)
