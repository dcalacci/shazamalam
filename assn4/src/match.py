import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate
from scipy.spatial import distance
import datetime
import read_audio

def downsample(stream):
    """ Downsample from 44100 -> 5512Hz
    """
    return decimate(stream, 8)

def get_mono(fpath):
    """ Converts the given wav file to 5512Hz PCM Mono
    """
    samplerate, channels = wavfile.read(fpath)
    return np.mean(channels, axis=1)

def fft(fpath):
    mono_stream = get_mono(fpath)
    return np.fft.fft(mono_stream)

def mse(A, B):
    return ((np.real(A) - np.real(B)) ** 2).mean()

def similarity(f1, f2):
    ffts = map(fft, [f1, f2])
    return mse(ffts[0], ffts[1])

"""
final_print:
prints match
"""
def final_print(audio_one_path, audio_two_path):
    print "MATCH: ", audio_one_path, " ", audio_two_path

"""
match_files:
Compares all files, prints matches

INPUT: 2 file arrays
OUTPUT: Prints all matches
"""
def match_files(a1, a2):
    for f1 in a1:
        for f2 in a2:
            result = is_match(f1,f2)
            if (result):
                final_print(f1,f2)

"""
is_match:
Returns a boolean if we deem that f1 and f2 match

INPUT: 2 files that are valid file paths
OUTPUT: True if we deem the files match, otherwise False
"""
def is_match(f1, f2):

    #preapre a string for our output
    match_threshold = 150000000000 # new threshold from new trial and error
    match_coefficient = 0

    # if ( is_mp3(f1) ) Determine if files are mp3
    #    f1_tmp = True
    #    os.system('lame -V2 --silent -decode ' + f1 + ' ' + new_wav_file_path) (or something like that)
    #    f1 = new_wav_file_path
    #
    # if ( is_mp3(f2) )
    #    f2_tmp = True
    #    os.system('lame -V2 --silent -decode ' + f2 + ' ' + new_wav_file_path) (or something like that)
    #    f2 = new_wav_file_path
    #

    """
    validate that the two files are of the same length
    """
    """TODO: Remove after ASSN 5"""
    if(read_audio.length(f1) != read_audio.length(f2)):
        return False
    else:
        # get our match coefficient!
        match_coefficient = similarity(f1, f2)

    #final print out to SDTOUT
    if(match_coefficient < match_threshold):
        return True
    else:
        return False

    # if ( f1_tmp )
    #    delete f1 tmp file

    # if ( f2_tmp )
    #    delete f2 tmp file
