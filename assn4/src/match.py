from collections import defaultdict
from os.path import basename
import fingerprinting
import read_audio
import datastore


# threshold for number of matching fingerprints in a given time offset
# to produce a match
MATCH_THRESHOLD = 60


def get_matches_for_hashes(hashes, dstore):
    """ hashes are a list of (md5, offset, time)
    Returns a list of (song_id, offset_diff) for each match.
    """
    # gets dict of md5 -> (offset, song_id, time)
    stored_hashes = dstore.get_fingerprints()

    # get all tuples that match our hashes.
    # matches will contain a list of tuples of the form:
    # (md5, database_offset, database_song_id)
    matches = []
    for h in hashes:
        if h[0] in stored_hashes:
            # list of tuples (multiple database songs with same hash)
            tuples = stored_hashes.get(h[0])
            matches.extend([(h[0],) + t for t in tuples])

    # create a dictionary of our query song offsets from the hashes
    # {hash: offset}
    query_offsets = {t[0]: t[1:] for t in hashes}

    # returns a list of (song_id, offset_diff, offset, query_offset)

    # offset_diff is the difference between the offset of the
    # fingerprint in the sample we've been given and the offset of the
    # corresponding fingerprint in the file in the datastore.

    res = []
    for h, db_offset, db_song_id, db_time in matches:
        query_offset = query_offsets[h][0]
        query_time = query_offsets[h][1]
        offset_diff = db_offset - query_offset
        res.append((db_song_id, offset_diff, db_offset, query_time, db_time))
    return res


def get_match(hash_tuples, dstore):
    """hash_tuples is a list of (MD5, offset) -> list of (songid, offset_dif)
    Assumes that what you're matching against is already in the datastore.
    """
    # (db_song_id, offset_diff, db_offset, query_time, db_time)
    matches = get_matches_for_hashes(hash_tuples, dstore)
    # make a dict of {song_name: {offset_diff: #collisions}}
    # then, we can iterate through the dict and choose songs that
    # have more than MATCH_THRESHOLD matches for some offset.
    song_offset_counter = defaultdict(lambda: defaultdict(int))
    for m in matches:
        song_id, offset_diff = m[:2]
        song_offset_counter[song_id][offset_diff] += 1

    likely_matches = []  # where we'll store all the matches
    for song_id, diff_dict in song_offset_counter.iteritems():
        offset_diff, max_count = max(diff_dict.iteritems(), key=lambda t: t[1])
        if max_count < MATCH_THRESHOLD:
            continue
        # append it to our list of likely matches.
        # we could also add a measure of confidence (how many matches
        # above our threshold)
        likely_matches.append((song_id, offset_diff))

    matches_to_return = []
    for song_id, offset_diff in likely_matches:
        # pick out hashes for which we have the right song id and the
        # right offset difference
        hashes = [match for match in matches
                  if match[0] == song_id and match[1] == offset_diff]

        # find minimum by offset
        start_peak = min(hashes, key=lambda t: t[2])
        query_start_time = start_peak[3]
        db_start_time = start_peak[4]

        end_peak = max(hashes, key=lambda t: t[2])
        query_end_time = end_peak[3]
        db_end_time = end_peak[4]

        query_duration = query_end_time - query_start_time
        db_duration = db_end_time - db_start_time

        # return the most likely song's ID and the start and end times:
        song_name = dstore.get_song_file_from_id(song_id)

        if query_duration > 5 and db_duration > 5:
            matches_to_return.append((song_name, query_start_time, db_start_time))
    return matches_to_return

def match_2_files(fpath1, fpath2):
    
    dstore = datastore.Datastore()

    #add first file
    dstore.add_fingerprints(fpath1)

    #match second file
    samples = read_audio.get_mono(fpath2)
    hashes = fingerprinting.get_fingerprints(samples)
    match_data = get_match(hashes, dstore)

    print match_data

    if len(match_data) == 0:
        return False
    else:
        match_data = match_data[0]
        return (match_data[2], match_data[1])

def is_match(f1, f2):
    """Returns True if f1 matches to f2.

    Currently works by comparing the number of matched fingerprints
    that occur at the same offset difference between the two songs.

    If this number is greater than MATCH_THRESHOLD, then it returns
    True.

    Wow, code reuse. Remind yourself to kick dan.
    Not very :herb:

    TODO: WHY IS THIS SO SLOW

    """
    mono1, mono2 = read_audio.get_mono(f1), read_audio.get_mono(f2)
    prints1, prints2 = [dict(fingerprinting.get_fingerprints(m))
                        for m in (mono1, mono2)]
    shared_hashes = set(prints1.keys()).intersection(set(prints2.keys()))

    # {offset_diff -> [(md5, offset1, offset2), ...]}
    offset_dict = defaultdict(list)
    match_counter = defaultdict(int)

    max_count = 0
    offset_difference = 0

    for h in shared_hashes:
        offset1, offset2 = prints1[h], prints2[h]
        offset_diff = abs(offset1 - offset2)
        offset_dict[offset_diff].append((h, offset1, offset2))
        match_counter[offset_diff] += 1
        count = match_counter[offset_diff]
        if count > max_count:
            max_count = count
            offset_difference = offset_diff

    if max_count > MATCH_THRESHOLD:
        hashes = match_counter[offset_difference]
        start1 = min(hashes, key=lambda t: t[1])[1]
        start2 = min(hashes, key=lambda t: t[2])[2]

        return (start1, start2)

    else:
        return False

def print_match(audio_1_path, match_data):
    """Prints matches according to black-box spec
    """

    for match in match_data:
        audio_2_path = match[0]
        time_1 = match[1]
        time_2 = match[2]

        # python will automatically include spaces between comma-deliniated elements
        print "MATCH", basename(audio_1_path).lstrip(), basename(audio_2_path).lstrip(), time_1, time_2
