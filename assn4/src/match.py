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
    
    averaged = list(np.mean(t) for t in zip(channels))
    
    return chunks(averaged, 100)

def fft(fpath):
    mono_stream = get_mono(fpath)
    print datetime.datetime.now(), "getting fft..."
    return map(np.fft.fft, mono_stream)

def mse(A, B):
    #convert from complex to real vectors
    A = map(convert, A)
    B = map(convert, B)
    #caluclate euclidean distance between A and B
    dist = [distance.euclidean(a,b) ** 2 for a, b in zip(A, B)]
    return np.mean(dist)

def convert(complx):
    return [complx.real, complx.imag]

def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

def similarity(f1, f2):
    
    f1_ffts = fft(f1)
    f2_ffts = fft(f2)
    
    print datetime.datetime.now(), "computing mse..."
    return min(map(mse, f1_ffts, f2_ffts))