import sys
import os
import unittest
import match

class TestAudioMatchingFunctions(unittest.TestCase):

	def test_is_match(self):
		print "Sit back and relax, this may take a while..."

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

		# Should not accept mp3 format
		self.run_is_match_test("../data/z05.wav", "../data/Sor3508.mp3", False)

		# Should return false when file doesn't exist
		self.run_is_match_test("../data/z05.wav", "../data/fakefile.wav", False)

	# running single is_match test
	def run_is_match_test(self, true_audio, suspect_audio, expected_is_match):
		if (expected_is_match):
			print "Testing that ", true_audio," and ", suspect_audio," match..."
		else:
			print "Testing that ", true_audio," and ", suspect_audio," DO NOT match..."

		# prevents printing
		sys.stdout = open(os.devnull, "w")

		actual_is_match = match.is_match(true_audio, suspect_audio)

		# ok now you can print again
		sys.stdout = sys.__stdout__

		if (expected_is_match):
			self.assertTrue(actual_is_match)
		else:
			self.assertFalse(actual_is_match)
		print "Test passed!"


# calls all test_* functions in TestAudioMatchingFunctions
unittest.main()
