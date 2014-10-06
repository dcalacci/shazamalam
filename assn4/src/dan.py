#!/usr/bin/env python
#import numpy
import read_wav
import fft
import getopt
import sys
import match

"""
This is the main executable file we'll run for assn4. 

Just testing fft for now or whatever
"""

"""
parse:
parse the files passed to us at the command line

INPUT: Command line arguments without the leading reference
OUTPUT: Duple of the file paths
"""
def parse_args(argv):

	#delcare audio file 1 (eventually artist audio?)
	true_audio = ""
	#delcare audio file 2 (eventually candidate audio?)
	suspect_audio = ""

	#temporary flag for checking which file is which
	true_audio_registered = False

	#get the audio arguments and options 
	try:
	  options, args = getopt.getopt(argv,"f:",["truefile=","suspectfile="])
   
	except getopt.GetoptError:
	  print 'dan.py -f <truefile> -f <suspectfile>'
	  sys.exit(2)

	#should we be given valid arguments, lets take a look
	for option, arg in options:
		#if its a file we were passed
		if option in ("-f", "--truefile"):
			#check the order it was passed in
			if not true_audio_registered:
				true_audio = arg
				true_audio_registered = True
			#otherwise
			else:
				suspect_audio = arg
				break

	return true_audio, suspect_audio

"""
final_print:
print out the final results 

NOTE: this is a process-terminating call
"""
def final_print(match, audio_one_path, audio_two_path):
	print match, audio_one_path, " ", audio_two_path
	sys.exit(0)

"""
main:
lets grab those input files shall we?

INPUT: Command line arguments without the leading reference
OUTPUT: Results of dan's main functionality a.k.a. commparing two audio files
"""
def main(argv):
	
	#delcare audio file 1 (eventually artist audio?)
	true_audio = ""
	#delcare audio file 2 (eventually candidate audio?)
	suspect_audio = ""
	#preapre a string for our output
	match_threshold = 10000000 #this is our trial and error threshold
	match_coefficient = 0

	#parse the audio files from the arguments
	true_audio, suspect_audio = parse_args(argv)

	#validate that these audio files are legit
	#formatcheckerrrr
	true_audio_is_wave = read_wav.validate_file(true_audio)
	suspect_audio_is_wave = read_wav.validate_file(suspect_audio)
	if (not (true_audio_is_wave and suspect_audio_is_wave)):
		return
	
	"""
	validate that the two files are of the same length
	"""
	"""TODO: Remove after ASSN 4"""
	if(read_wav.length(true_audio) != read_wav.length(suspect_audio)):
		final_print("NO MATCH", true_audio, suspect_audio)
	else:
		#now lets read those wave files
		true_signal, true_sample = read_wav.mono_channel(true_audio)
		suspect_signal, suspect_sample = read_wav.mono_channel(suspect_audio)

		#look at the fft, oh my theres a lot of info huh
		match_coefficient = match.similarity(true_audio, suspect_audio) / true_sample

	#final print out to SDTOUT
	if(match_coefficient < match_threshold):
		final_print("MATCH", true_audio, suspect_audio)
	else:
		final_print("NO MATCH", "", "")

#run maine (1: lops off the leading reference)
main(sys.argv[1:])