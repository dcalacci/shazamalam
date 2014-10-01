#!/usr/bin/env python
#import numpy
import read_wav
import fft
import getopt
import sys

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

	#for now, just print out the files
	print "true audio = ", true_audio
	print "suspect audio = ", suspect_audio

	#now lets read those wave files
	true_signal, true_sample = read_wav.mono_channel(true_audio)
	suspect_signal, suspect_sample = read_wav.mono_channel(suspect_audio)

	#look at the fft, oh my theres a lot of info huh
	print true_sample#fft.fft(true_signal)

#run maine (1: lops off the leading reference)
main(sys.argv[1:])