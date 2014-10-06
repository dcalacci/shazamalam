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
	  options, args = getopt.getopt(argv,"f:f:",["truefile=","suspectfile="])

	  #check number of options
	  if(len(options) < 2):
	  	print 'ERROR: incorrect command line'
	  	sys.exit(2)
   
	except getopt.GetoptError:
	  print 'ERROR: incorrect command line'
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

	#parse the audio files from the arguments
	true_audio, suspect_audio = parse_args(argv)

	"""
	TODO:
	In the future, parse_args will handle collecting 
	entire directories instead
	"""
	result = match.is_match(true_audio, suspect_audio)

	if(result):
		final_print("MATCH", true_audio, suspect_audio)
	else:
		final_print("NO MATCH", true_audio, suspect_audio)

#run maine (1: lops off the leading reference)
main(sys.argv[1:])