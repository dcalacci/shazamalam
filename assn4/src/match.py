from collections import defaultdict
from os.path import basename
from datastore import *


def get_matches_for_hashes(hashes):
    """ hashes are a list of (md5, offset)
    Returns a list of (song_id, offset_diff) for each match.
    """

    # list of (md5, offset, song_id)
    lines = [l.strip() for l in open(FINGERPRINT_FILE, 'rb').readlines()]
    lines = [line.split('|') for line in lines]

    # create dict of md5 -> (offset, song_id)
    # get all tuples that match our hashes
    stored_hashes = {t[0]: map(int, t[1:]) for t in lines}
    matches = [(h[0], stored_hashes.get(h[0])) for h in hashes if h[0] in stored_hashes]
    matches = [[m[0], m[1][0], m[1][1]] for m in matches]

    query_offsets = dict(hashes)

    # list of (song_id, offset_diff)
    # we compute the difference between the offset of this match in our database
    # and the offset of the given sample.
    return [(song_id, offset - query_offsets[h]) for h, offset, song_id in matches]


def get_matches(hash_tuples):
    """list of (MD5, offset) -> list of (songid, offset_dif)
    Assumes that what you're matching against is already in the datastore.
    """
    most_likely_song = (None, 0)
    # {offset_diff: {song_id: #collisions} ...}
    match_counter = defaultdict(lambda: defaultdict(int))
    # (song_id, offset_diff)
    matches = get_matches_for_hashes(hash_tuples)
    for song_id, offset_diff in matches:
        match_counter[offset_diff][song_id] += 1
        # update the most likely song if the highest count changes.
        count = match_counter[offset_diff][song_id]
        if count > most_likely_song[1]:
            most_likely_song = (song_id, count)
    # return the most likely song's ID
    return most_likely_song[0]


MATCH_THRESHOLD = 5

def is_match(f1, f2):
    """Returns True if f1 matches to f2.

    Currently works by comparing the number of matched fingerprints
    that occur at the same offset difference between the two songs.

    If this number is greater than MATCH_THRESHOLD, then it returns
    True.

    Wow, code reuse. Remind yourself to kick dan.
    Not very :herb:
    """
    mono1, mono2 = read_audio.get_mono(f1), read_audio.get_mono(f2)
    fingerprints = [fingerprinting.get_fingerprints(m) for m in (mono1, mono2)]

    # {offset_diff -> {fingerprint -> count}}
    match_counter = defaultdict(int)
    max_count = 0
    for print1, offset1 in fingerprints[0]:
        for print2, offset2 in fingerprints[1]:
            if print1 == print2:
                offset_diff = abs(offset1 - offset2)
                match_counter[offset_diff] += 1
                count = match_counter[offset_diff]
                if count > max_count:
                    max_count = count
    if max_count > MATCH_THRESHOLD:
        return True


def final_print(audio_1_path, audio_2_path):
    """Prints matches according to black-box spec
    """
    print "MATCH: ", basename(audio_1_path), " ", basename(audio_2_path)




# """
# is_match:
# Returns a boolean if we deem that f1 and f2 match

# INPUT: 2 files that are valid file paths
# OUTPUT: True if we deem the files match, otherwise False
# """
# def is_match(f1, f2):

#     #preapre a string for our output
#     match_threshold = 150000000000 # new threshold from new trial and error
#     match_coefficient = 0

#     if ( read_audio.is_mp3(f1) ):
#         f1 = read_audio.create_temp_wav_file(f1)

#     if ( read_audio.is_mp3(f2) ):
#         f2 = read_audio.create_temp_wav_file(f2)

#     """
#     validate that the two files are of the same length
#     """
#     """TODO: Remove after ASSN 5"""
#     if(read_audio.length(f1) != read_audio.length(f2)):
#         read_audio.delete_temp_file(f1) # only deletes if /tmp is in filepath
#         read_audio.delete_temp_file(f2)
#         return False
#     else:
#         # get our match coefficient!
#         match_coefficient = similarity(f1, f2)
#         read_audio.delete_temp_file(f1) # only deletes if /tmp is in filepath
#         read_audio.delete_temp_file(f2)

#     #final print out to SDTOUT
#     if(match_coefficient < match_threshold):
#         return True
#     else:
#         return False


# """
# match_files:
# Compares all files, prints matches

# INPUT: 2 file arrays
# OUTPUT: List of matches as tuples, also prints all matches
# """
# def match_files(a1, a2):
#     matches = []
#     for f1 in a1:
#         for f2 in a2:
#             result = is_match(f1,f2)
#             if (result):
#                 matches.append((f1,f2))
#                 final_print(f1,f2)
#     return matches

# """
# is_match:
# Returns a boolean if we deem that f1 and f2 match

# INPUT: 2 files that are valid file paths
# OUTPUT: True if we deem the files match, otherwise False
# """
# def is_match(f1, f2):

#     #preapre a string for our output
#     match_threshold = 150000000000 # new threshold from new trial and error
#     match_coefficient = 0

#     if ( read_audio.is_mp3(f1) ):
#         f1 = read_audio.create_temp_wav_file(f1)

#     if ( read_audio.is_mp3(f2) ):
#         f2 = read_audio.create_temp_wav_file(f2)

#     """
#     validate that the two files are of the same length
#     """
#     """TODO: Remove after ASSN 5"""
#     if(read_audio.length(f1) != read_audio.length(f2)):
#         read_audio.delete_temp_file(f1) # only deletes if /tmp is in filepath
#         read_audio.delete_temp_file(f2)
#         return False
#     else:
#         # get our match coefficient!
#         match_coefficient = similarity(f1, f2)
#         read_audio.delete_temp_file(f1) # only deletes if /tmp is in filepath
#         read_audio.delete_temp_file(f2)

#     #final print out to SDTOUT
#     if(match_coefficient < match_threshold):
#         return True
#     else:
#         return False
