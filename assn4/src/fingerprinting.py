import numpy as np
from scipy.io import wavfile
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, iterate_structure, binary_erosion
import hashlib


WINDOW_SIZE = 4096 # granularity of chunks
SAMPLE_RATE = 44100 # by nyquist or whatever
OVERLAP_RATIO = 0.5 # amount our chunks can overlap

def get_fingerprints(samples):
    spectrogram = plt.specgram(mono,
                               NFFT=WINDOW_SIZE,
                               Fs=SAMPLE_RATE,
                               window=mlab.window_hanning,
                               noverlap = int(WINDOW_SIZE * OVERLAP_RATIO))[0]
    # log the result
    spectrogram = 10 * np.log10(spectrogram)

    # np.inf is terrible, replace with zeros.
    spectrogram[spectrogram == -np.inf] = 0


AMPLITUDE_THRESHOLD = 20

def get_peaks(spectrogram):
    """Gets all the peaks from this spectrogram.
    """
    # generate the filter pattern (neighborhoods)
    peak_filter = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(peak_filter, 20).astype(int)

    # set each point equal to the maximum in it's neighborhood
    local_max = maximum_filter(spectrogram, footprint=neighborhood)

    # check where the 'local max' is equal to our original values.
    # these are our peaks.
    peaks = local_max==spectrogram

    # filter out background around the peaks:
    # http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.morphology.binary_erosion.html
    background = (spectrogram == 0)
    eroded = binary_erosion(background,
                            structure=neighborhood,
                            border_value=1)
    actual_peaks = peaks - eroded

    # problem here is that we see lots of peaks in LOW areas. Let's
    # filter out the low ones.
    amplitudes = spectrogram[actual_peaks].flatten()
    y, x = actual_peaks.astype(type).nonzero()
    all_peaks = zip(x, y, amplitudes)

    filtered_peaks = [p for p in all_peaks if p[2] > AMPLITUDE_THRESHOLD]

    # great, now we can return the peaks as the two (time, frequency) lists for each peak:
    return ([p[0] for p in filtered_peaks],
            [p[1] for p in filtered_peaks])


# # Fingerprinting
# 194 is a good feature reduction from thousasnds of samples, I think :).
# 
# Next step: how do we use these peaks to find matches?
# 
# Well, really, a song can be thought of a series of pairs of peaks, separated by a time value.
# 
# We can fingerprint a song by creating a series of hashed (peak_freq_1, peak_freq_2, time_delta) tuples.
# 
# Then, when we look for matches for a given song $B$, we can:
#  1. fingerprint song B, collecting a series of $N$ hashed (peak_freq_1, peak_freq_2, time_delta) tuples (let's call them $t_i$).
#  2.  $\forall i \in N$ for song $B$, check if we have a hash collision for $t_i$ from our stored files.
#  3.  Check which song file has the most hash collisions (maybe set a threshold?). If the number of collisions for some file is above our threshold, return that song as a match.
#  
# First, we need to define how many pairs of peaks are created for each individual peak. Let's use $\frac{N}{10}$ to start:

# In[65]:

fingerprint_pairs = 19


# We also need to define a time range - we don't want one peak to be paired with another if they're too far apart in time. maybe 10 is good?

# In[64]:

fingerprint_time_delta = 10


# Okay, let's actually make the fingerprints. This can probably be faster.

# In[86]:

# sort by time (I think the other guy does it by frequency? not sure why...)
sorted_peaks = sorted(filtered_peaks, key=lambda p: p[0])

# of the form (f1, f2, time_delta)
fingerprints = []
for i, peak in enumerate(sorted_peaks):
    # get all peaks within `fingerprint_pairs` of the current peak
    potential_pairs = sorted_peaks[i+1:i+fingerprint_pairs]
    # get rid of the ones that are too far away in time
    potential_pairs = [p for p in potential_pairs if p[0] - peak[0] < fingerprint_time_delta]
    # create the (f1, f2, time_delta) tuples
    prints = [(peak[1], p[1], (p[0] - peak[0])) for p in potential_pairs]
    fingerprints.extend(prints)    


# Okay, how many fingerprints is that?

# In[68]:

len(fingerprints)


# Still not bad. These are gonna be hashes, remember, and this is the whole song.
# 
# Let's just check what they look like:

# In[73]:

fingerprints[:10]


# I'm not sure about having pairs at time_delta == 0, but I'll leave them there for now.
# 
# Okay, great. Now we just have to hash them....
# 
# MD5?

# In[81]:

hashes = []
for fprint in fingerprints:
    h = hashlib.md5('{0}|{1}|{2}'.format(fprint[0], fprint[1], fprint[2]))
    hashes.append(h.hexdigest())


# Okay, what do they look like?

# In[83]:

hashes[:5]


# Cool! Now, there's just the question of how we're going to do efficient searches of these hashes and stuff. 
# 
# Can we use a database? Is that cheating? not sure...
