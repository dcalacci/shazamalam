#!/usr/bin/env python
import wave
import struct
import collections


def mean(ns):
    return float(sum(ns) / len(ns))


def _byte_format(sample_width, num_samples):
    """Produces the byte format string for the given sample width and
    number of samples.

    """
    # formatting for reading byte info from wave library
    if sample_width == 1:
        return "%iB" % num_samples  # read unsigned chars
    elif sample_width == 2:
        return "%ih" % num_samples  # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

def length(wave_file):
    wr = wave.open(wave_file, "rb")
    sample_rate = wr.getframerate()
    num_frames = wr.getnframes()
    wr.close()

    return num_frames / float(sample_rate);

def mono_channel(wave_file):
    """Given a file-like object or file path representing a wave file,
    decompose it into its constituent PCM data streams.

    Input: A file like object or file path
    Output: A list of lists of integers representing the PCM coded
        data stream channels and the sample rate of the channels
        (mixed rate channels not supported)
    """
    wr = wave.open(wave_file, "rb")
    num_channels = wr.getnchannels()
    sample_rate = wr.getframerate()
    sample_width = wr.getsampwidth()
    num_frames = wr.getnframes()
    raw_data = wr.readframes(num_frames)  # Returns byte data
    wr.close()

    num_samples = num_frames * num_channels

    # unpack byte data into int data
    bf = _byte_format(sample_width, num_samples)
    int_data = struct.unpack(bf, raw_data)

    # we want to separate the data into the different channels
    # create mono stream - first, split into all channels, then average.

    channels = [[]] * num_samples  # initialize empty list

    def get_channel(index):
        return index % num_channels

    for index, val in enumerate(int_data):
        channels[get_channel(index)].append(val)

    # create the mono stream by averaging all the channels.  we'd like
    # to support more than two channels - the zip implementation does
    # this, but slowly for some reason

    # why is this slower than the thing that's uncommented?
    # mono_stream = [mean(t) for t in izip(*channels)]
    mono_stream = [mean([channels[0][n], channels[1][n]]) for n in range(num_samples)]

    return mono_stream, sample_rate
