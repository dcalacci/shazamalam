import numpy as np
from scipy.io import wavfile
from scipy.signal import decimate
from scipy.spatial import distance
import datetime

def downsample(stream):
    """ Downsample from 44100 -> 5512Hz
    """
    return decimate(stream, 8)

def get_mono(fpath):
    """ Converts the given wav file to 5512Hz PCM Mono
    """
    print datetime.datetime.now(), "reading file..."
    samplerate, data = wavfile.read(fpath)
    #print datetime.datetime.now(), "downsampling..."
    #channels = map(downsample, data)
    channels = data
    print datetime.datetime.now(), "converting to mono..."
    return list(np.mean(t) for t in zip(channels))

def fft(fpath):
    mono_stream = get_mono(fpath)
    print datetime.datetime.now(), "getting fft..."
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
    print datetime.datetime.now(), "computing mse..."
    return mse(ffts[0], ffts[1])
