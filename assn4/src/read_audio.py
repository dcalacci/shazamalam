#!/usr/bin/env python
from scipy.io import wavfile
import numpy as np
import wave
import os
import sys
import subprocess


def get_mono(fpath):
    """ Converts the given wav file to 44100 PCM Mono.
    """
    if is_mp3(fpath):
        fpath = create_temp_wav_file(fpath)
    samplerate, channels = wavfile.read(fpath)

    # if it's mono
    if type(channels[0]) != np.ndarray:
        return channels

    if samplerate != 44100:
        raise Exception("File at " + fpath + " isn't 44100 sample rate, breaking...")

    # TODO: Handle mono files correctly.

    return np.mean(channels, axis=1)


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
    format_string = "MPEG"
    layer_string = "layer III"
    version_string = "v1"
    # currently does not include version
    if format_string not in file_header or layer_string not in file_header:
        return False

    # otherwise
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
                print "Program terminating..."
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
        print "ERROR: file ", short_name, " does not exist"
    except wave.Error:
        if is_mp3(file_input):
            return True

        print "ERROR: file ", short_name, " is not a supported format"
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
        print "ERROR: directory ", short_name, " does not exist"
    return False


def length(wave_file):
    wr = wave.open(wave_file, "rb")
    sample_rate = wr.getframerate()
    num_frames = wr.getnframes()
    wr.close()

    return num_frames / float(sample_rate)


def create_temp_wav_file(file_path):
    """Creates a temporary wav file from the given mp3 file.

    Returns the full path of the temporary wav file.
    """
    path_array = file_path.split('/')
    filename = path_array[-1]
    new_wav_file_path = '/tmp/' + filename.split('.')[0] + '.wav'
    # test if user has lame in system, do subprocess call
    # output to /dev/null
    FNULL = open(os.devnull, 'w')
    res = subprocess.call(['/usr/bin/env', 'lame'],
                          stdout=FNULL,
                          stderr=subprocess.STDOUT)
    if res == 1:
        lame_cmd = ['/usr/bin/env', 'lame']
    else:
        lame_cmd = ['/course/cs4500f14/bin/lame']
    args = ['-V2', '--silent', '--decode', file_path, new_wav_file_path]
    res = subprocess.call(lame_cmd + args,
                          stdout=FNULL,
                          stderr=subprocess.STDOUT)

    if res != 0:
        raise Exception("Call to lame failed. It's either not installed or it failed the conversion.")

    return new_wav_file_path


def delete_temp_file(file_path):
    if '/tmp' in file_path:
        os.system('rm -f ' + file_path)
