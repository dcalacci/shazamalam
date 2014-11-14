import fingerprinting
import read_audio
import os
from collections import defaultdict

SONG_ID_FILE = "/tmp/songs.txt"
FINGERPRINT_FILE = "/tmp/fingerprints.txt"


class Datastore():
    """Stores all the relevant data for performing song copy lookups.
    """
    def __init__(self):
        self.FINGERPRINTS = defaultdict(list)
        self.SONGS = []

    def song_is_saved(self, fpath):
        return fpath in self.SONGS

    def save_song(self, fpath):
        """Saves the given song.
        Each line is the filepath to a particular song.
        The line number in the file is it's ID.
        Returns the ID of the given song path.
        """
        if not self.song_is_saved(fpath):
            self.SONGS.append(fpath)
        return self.SONGS.index(fpath)

    def add_fingerprints(self, fpath):
        """Processes the given file.
         - saves the song in the file 'database'
         - processes all the fingerprints, saves them in the fingerprints file
        """
        if self.song_is_saved(fpath):
            return
        song_id = self.save_song(fpath)
        samples = read_audio.get_mono(fpath)
        fingerprints = fingerprinting.get_fingerprints(samples)

        for md5, offset, time in fingerprints:
            self.FINGERPRINTS[md5].append((offset, song_id, time))

    def get_fingerprints(self):
        return self.FINGERPRINTS

    def get_song_file_from_id(self, song_id):
        return self.SONGS[song_id]
