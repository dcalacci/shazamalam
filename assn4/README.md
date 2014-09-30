# Assignment 4

Assignment 4 specifies that we create a program, named dan, that can
tell if two audio files are the same.

This is gonna tell if they're EXACTLY the same, not 70% or 80%.

The files we're given have the same audio, just bit-shifted, or something.

## Plan

1. convert to PCM, mono

2. do FFT on these suckers, grabbing frequency space

3. compare frequency/magnitude vectors??
