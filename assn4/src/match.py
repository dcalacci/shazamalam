import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate
from scipy.spatial import distance
import datetime
import read_wav

def downsample(stream):
    """ Downsample from 44100 -> 5512Hz
    """
    return decimate(stream, 8)

def get_mono(fpath):
    """ Converts the given wav file to 5512Hz PCM Mono
    """
    #print datetime.datetime.now(), "reading file..."
    samplerate, data = wavfile.read(fpath)
    #print datetime.datetime.now(), "downsampling..."
    #channels = map(downsample, data)
    channels = data
    #print datetime.datetime.now(), "converting to mono..."
    return list(np.mean(t) for t in zip(channels))

def fft(fpath):
    mono_stream = get_mono(fpath)
    #print datetime.datetime.now(), "getting fft..."
    return np.fft.fft(mono_stream)

def mse(A, B):
    #convert from complex to real vectors
    A = map(convert, A)
    B = map(convert, B)
    #caluclate euclidean distance between A and B
    dist = [distance.euclidean(a,b) ** 2 for a, b in zip(A, B)]
    return np.mean(dist)

def convert(complx):
    return [complx.real, complx.imag]

def similarity(f1, f2):
    ffts = map(fft, [f1, f2])
    #print datetime.datetime.now(), "computing mse..."
    return mse(ffts[0], ffts[1])

"""
is_match: 
Returns a boolean if we deem that f1 and f2 match

INPUT: 2 files that may or MAY NOT be valid file paths
OUTPUT: True if we deem the files match, otherwise False
"""
def is_match(f1, f2):
    
    #preapre a string for our output
    match_threshold = 10000000 #this is our trial and error threshold
    match_coefficient = 0

    #validate that these audio files are legit
    if (not (read_wav.validate_file(f1) and read_wav.validate_file(f2))):
        return #validate file will handle error messages if validation fails
    
    """
    validate that the two files are of the same length
    """
    """TODO: Remove after ASSN 4"""
    if(read_wav.length(f1) != read_wav.length(f2)):
        return False
    else:
        #now lets read those wave files
        true_signal, true_sample = read_wav.mono_channel(f1)
        suspect_signal, suspect_sample = read_wav.mono_channel(f2)

        #look at the fft, oh my theres a lot of info huh
        match_coefficient = similarity(f1, f2) / true_sample

    #final print out to SDTOUT
    if(match_coefficient < match_threshold):
        return True
    else:
        return False
