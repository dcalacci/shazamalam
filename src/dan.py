#!/usr/bin/env python
#import numpy
import read_audio
import getopt
import sys
import match
import datastore
import fingerprinting


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
      option_value_hash, command_line_args = getopt.getopt(argv,"f:d:")
      # not using command_line_args, arguments in 
      # options_value_hash (-option => argument)

      #check number of options
      if(len(option_value_hash) < 2):
        sys.stderr.write('ERROR incorrect command line arguments \n')
        sys.exit(2)

    except getopt.GetoptError:
      sys.stderr.write('ERROR incorrect command line arguments \n')
      sys.exit(2)

    #should we be given valid arguments, lets take a look
    for option, arg in option_value_hash:
        #if its a file we were passed
        if option in ("-f", "-d"):
            #check the order it was passed in
            if not true_audio_registered:
                true_audio = (option, arg)
                true_audio_registered = True
            #otherwise
            else:
                suspect_audio = (option, arg)
                break


    return true_audio, suspect_audio


"""
main:
lets grab those input files shall we?

INPUT: Command line arguments without the 
       leading reference
OUTPUT: Results of dan's main functionality 
        a.k.a. commparing two audio files
"""
def main(argv):

    #delcare audio file 1 (eventually artist audio?)
    true_audio = ""
    #delcare audio file 2 (eventually candidate audio?)
    suspect_audio = ""

    #parse the audio files from the arguments
    true_audio, suspect_audio = parse_args(argv)

    #validate that these audio files are legit
    if (not (read_audio.validate_input(true_audio) and 
        read_audio.validate_input(suspect_audio))):
        sys.exit(2)

    dstore = datastore.Datastore()

    true_audio = read_audio.create_file_array(true_audio)
    suspect_audio = read_audio.create_file_array(suspect_audio)

    for suspect_audio_path in suspect_audio:
        dstore.add_fingerprints(suspect_audio_path)

    for true_audio_path in true_audio:
        samples = read_audio.get_mono(true_audio_path)
        hashes = fingerprinting.get_fingerprints(samples)
        match_data = match.get_match(hashes, dstore, true_audio_path)
        match.print_match(true_audio_path, match_data)

#run maine (1: lops off the leading reference)
try:
    main(sys.argv[1:])
except:
    sys.exit(2)
