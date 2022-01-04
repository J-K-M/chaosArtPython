# chaosArtPython
A python application to generate interesting images. 
(Inspired by https://www.youtube.com/watch?v=fDSIRXmnVvk)

The most notable files in this repo are interactive.py (in the chunkMethod folder)
and processingGifMaker.py (in the threading folder)

interactive.py allows for near realtime exploration of pairs of equations and is useful
for identifying interesting ranges of t values.

processingGifMaker.py is the third itteration of gifMaker which uses the multiprocessing
library to parallelize frame rendering.
The first version used only a single thread and the second version did implement threading
however due to the nature of this processing workload having multiple threads didn't give
much higher performance. (Because the threads do not actually process in parallel)
