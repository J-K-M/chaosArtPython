# chaosArtPython
A python application to generate interesting images. 
(Inspired by https://www.youtube.com/watch?v=fDSIRXmnVvk)

chunkMethod contains a version of the code which splits image rendering into small chunks and performs these
chunks in the main tkinter loop (giving tkinter time to update the screen)

threadMethod contains a version of the code which splits image rendering into a seperate thread to the main 
tkinter gui.
