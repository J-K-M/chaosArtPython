# chaosArtPython
A python application to generate interesting images. 
(Inspired by https://www.youtube.com/watch?v=fDSIRXmnVvk)

The most notable files in this repo are interactive.py (in the interactiveExplorer folder)
and clipMaker.py 
interactive.py allows for near realtime exploration of pairs of equations and is useful
for identifying interesting ranges of t values.
These equations and t values can then be used in clipMaker.py to render high quality videos
or gifs that show how the images created by the equations evolve over changing t values.

clipMaker.py uses the multiprocessing library to parallelize frame rendering making it a
faster, more featurefull version of oldGifMaker.py (which is single threaded).
