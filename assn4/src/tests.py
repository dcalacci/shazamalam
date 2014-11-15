import sys
import os
import unittest
import match
import read_audio

class TestAudioMatchingFunctions(unittest.TestCase):

	def test_is_match(self):
		print "****Hey let's match some files"

		#IM COMMENTING THIS OUT BECAUSE ITS OLD DATA GAHHH
		"""
		# Should return false when file doesn't exist
		self.run_is_match_test("../data/z05.wav", "../data/fakefile.wav", False)

		# Should be matches
		self.run_is_match_test("../data/z01.wav", "../data/z02.wav", True)
		self.run_is_match_test("../data/z03.wav", "../data/z04.wav", True)
		self.run_is_match_test("../data/z05.wav", "../data/z06.wav", True)
		self.run_is_match_test("../data/z07.wav", "../data/z08.wav", True)
		self.run_is_match_test("../data/z07.wav", "../data/Sor4959.wav", True)
		self.run_is_match_test("../data/z05.wav", "../data/Sor1929.wav", True)
		self.run_is_match_test("../data/z03.wav", "../data/bad2131.wav", True)
		self.run_is_match_test("../data/z02.wav", "../data/bad0616.wav", True)
		"""

		# Testing matches with certain time stamps
		self.run_is_match_test_timestamp("../D3/mMbm.wav", "../D3/bad_guy_in_yer_bar.wav", 44.6, 17.8, True) #MATCH mMbm.wav bad_guy_in_yer_bar.wav 44.6 17.8
		self.run_is_match_test_timestamp("../D3/mmsm.wav", "../D3/Sor3508.wav", 35.6, 36.8, True) #MATCH mmsm.wav Sor3508.wav 35.6 36.8
		self.run_is_match_test_timestamp("../D3/MMw.wav", "../D3/WhoopeeTiYiYo.wav", 74.8, 40.0, True) #MATCH MMw.wav WhoopeeTiYiYo.wav 74.8 40.0
		self.run_is_match_test_timestamp("../D3/Mpmm.wav", "../D3/Piste1.wav", 37.4, 101.0, True) #MATCH Mpmm.wav Piste1.wav 37.4 101.0

		"""
		# Should NOT be matches
		self.run_is_match_test("../data/z02.wav", "../data/z03.wav", False)
		self.run_is_match_test("../data/z04.wav", "../data/z05.wav", False)
		self.run_is_match_test("../data/z06.wav", "../data/z07.wav", False)
		self.run_is_match_test("../data/z05.wav", "../data/Sor3508.wav", False)
		self.run_is_match_test("../data/Sor4959.wav", "../data/Sor1929.wav", False)
		self.run_is_match_test("../data/z02.wav", "../data/bad2131.wav", False)
		self.run_is_match_test("../data/z03.wav", "../data/bad0616.wav", False)

		# Should accept mp3 format
		self.run_is_match_test("../data/Sor3508.wav", "../data/Sor3508.mp3", True)
		"""

	# tests directories
	"""
	We don't have very good test data to test this against so, its axed 
	for now sorry guys
	"""
	# def test_match_files(self):
	# 	print "****Hey let's match some directories"

	# 	z01 = '../data/z01.wav'
	# 	z02 = '../data/z02.wav'
	# 	bad0616 ='../data/bad0616.wav'
	# 	expected_matches = [(z02, bad0616), (z02, z01), (z02, z02)]

	# 	self.run_match_files_test(("-f", "../D1/z02.wav"), ("-d", "../data"), expected_matches)

	# running single is_match test
	def run_is_match_test(self, true_audio, suspect_audio, expected_is_match):
		if (expected_is_match):
			print "Testing that ", true_audio," and ", suspect_audio," match..."
		else:
			print "Testing that ", true_audio," and ", suspect_audio," DO NOT match..."

		# prevents printing
		sys.stdout = open(os.devnull, "w")

		actual_is_match = self.is_match_with_validation(true_audio, suspect_audio)

		# ok now you can print again
		sys.stdout = sys.__stdout__

		if (expected_is_match):
			self.assertTrue(actual_is_match)
		else:
			self.assertFalse(actual_is_match)
		print "Test passed!"

	# running single is_match test with time threshhold bounds
	def run_is_match_test_timestamp(self, true_audio, suspect_audio, true_time, suspect_time, expected_is_match, threshhold=10):
		if (expected_is_match):
			print "Testing that", true_audio,"and", suspect_audio,"match within",threshhold,"seconds ..."
		else:
			print "Testing that", true_audio,"and", suspect_audio,"DO NOT MATCH within",threshhold,"seconds ..."

		# prevents printing
		sys.stdout = open(os.devnull, "w")

		"""
		TODO: write a version of is_match_with_validation that returns if its a
		match and the start times of the true and suspect audio files
		"""
		actual_is_match = False
		match_data = self.match_with_time(true_audio, suspect_audio)

		if(match_data != False):
			true_time_match = (true_time - threshhold <= match_data[0]) and (true_time + threshhold >= match_data[0])
			suspect_time_match = (suspect_time - threshhold <= match_data[1]) and (suspect_time + threshhold >= match_data[1])
			actual_is_match = true_time_match and suspect_time_match

		# ok now you can print again
		sys.stdout = sys.__stdout__

		if (expected_is_match):
			self.assertTrue(actual_is_match)
		else:
			self.assertFalse(actual_is_match)
		print "Test passed!"

	# tests match_files, takes tuples
	def run_match_files_test(self, true_audio, suspect_audio, expected_matches):
		print "Testing ", true_audio," against ", suspect_audio," ..."

		# prevents printing
		sys.stdout = open(os.devnull, "w")

		actual_matches = self.match_files_with_validation(true_audio, suspect_audio)

		# ok now you can print again
		sys.stdout = sys.__stdout__

		self.assertEquals(expected_matches, actual_matches)

		print "Test passed!"

	def match_files_with_validation(self, f1, f2):
		f1_valid = read_audio.validate_input(f1)
		f2_valid = read_audio.validate_input(f2)
		if (f1_valid and f2_valid):
			f1 = read_audio.create_file_array(f1)
			f2 = read_audio.create_file_array(f2)
			return match.match_files(f1,f2)
		else:
			return []

	def match_with_time(self, f1, f2):
		f1_valid = read_audio.validate_file(f1)
		f2_valid = read_audio.validate_file(f2)
		if (f1_valid and f2_valid):

			"""
			this might be overkill? should be wrapped up
			more conveniently IMO

			basically mimic what dan.py does to prep match comparison
			
			======

			#create a fresh new data store and add f2's fingerprints
			dstore = datastore.Datastore()
			dstore.add_fingerprints(f2)

			#sample and get the fingerprint hashes for f1
			samples = read_audio.get_mono(f1)
			hashes = fingerprinting.get_fingerprints(samples)

			# get the juicy, juicy match data we want so bad
			match_data = match.get_match(hashes, dstore)
			# (song_name, query_start_time, db_start_time)


			if(len(match_data) > 0):
				print match_data
				return (True, match_data[1], match_data[2])
			else:
				return (False, -1, -1)


			"""
			#print "match_with_time:", f1, f2, match.is_match(f1, f2)
			return match.is_match(f1, f2)

# calls all test_* functions in TestAudioMatchingFunctions
unittest.main()
