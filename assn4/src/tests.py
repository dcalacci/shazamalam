import sys
import os
import unittest
import match

class TestAudioMatchingFunctions(unittest.TestCase):

	def test_mse(self):
		self.run_mse_test("../data/z01.wav", "../data/z02.wav", 495200)

	# running single mse_test
	def run_mse_test(self, true_audio, suspect_audio, expected_mse):
		# prevents printing
		sys.stdout = open(os.devnull, "w")

		actual_mse = match.similarity(true_audio, suspect_audio)
		actual_mse = int(actual_mse)

		# ok now you can print again
		sys.stdout = sys.__stdout__

		self.assertEqual(expected_mse, actual_mse)


# calls all test_* functions in TestAudioMatchingFunctions
def run_tests():
	unittest.main()

run_tests()