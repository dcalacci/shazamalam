import fingerprinting
import read_audio
import os

SONG_ID_FILE = "/tmp/songs.txt"
FINGERPRINT_FILE = "/tmp/fingerprints.txt"


def get_fingerprints():
    """Retrieves all the stored fingerprints.
    Returns a list of tuples. Each tuple is of the form:

    (md5, offset, song_id)
    """
    lines = [l.strip() for l in open(FINGERPRINT_FILE, 'rb').readlines()]
    lines = [line.split('|') for line in lines]
    return lines


def save_song(fpath):
    """Saves the given song.
    Each line is the filepath to a particular song.
    The line number in the file is it's ID.
    Returns the ID of the given song path.
    """
    # if the song is already stored
    if os.path.basename(SONG_ID_FILE) in os.listdir('/tmp'):
        files = [l.strip() for l in open(SONG_ID_FILE, 'rb').readlines()]
        if fpath in files:
            return files.index(fpath)

    with open('/tmp/songs.txt', 'a') as outfile:
        outfile.write(fpath + '\n')

    song_id = len(open(SONG_ID_FILE, 'rb').readlines()) - 1
    return song_id


def save_fingerprints(fprints, song_id):
    """Saves all the fingerprints for the given song id to the
    fingerprints file.

    Each line in the fingerprints file corresponds to one fingerprint.
    It's formatted as follows:
    MD5|OFFSET|SONG_ID
    """
    with open(FINGERPRINT_FILE, 'a') as outfile:
        for md5, offset, offset_times in fprints:
            outfile.write("{0}|{1}|{2}|{3}\n".format(md5, 
                                                  offset, 
                                                  song_id, 
                                                  offset_times))


def add_fingerprints(fpath):
    """Processes the given file.
     - saves the song in the file 'database'
     - processes all the fingerprints, saves them in the fingerprints file
    """
    song_id = save_song(fpath)
    samples = read_audio.get_mono(fpath)
    fingerprints = fingerprinting.get_fingerprints(samples)
    save_fingerprints(fingerprints, song_id)


def get_song_file_from_id(song_id):
    # might have to strip lines?
    songs = open(SONG_ID_FILE).readlines()
    return songs[int(song_id)]
