import sys
import os
import unittest
import match
import read_audio

class TestAudioMatchingFunctions(unittest.TestCase):

	def test_is_match(self):

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

	def is_match_with_validation(self, f1, f2):
		f1_valid = read_audio.validate_file(f1)
		f2_valid = read_audio.validate_file(f2)
		if (f1_valid and f2_valid):
			return match.is_match(f1,f2)
		else:
			return False


# calls all test_* functions in TestAudioMatchingFunctions
unittest.main()
