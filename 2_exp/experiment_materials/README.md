# Materials

This folder is meant to hold all materials needed to run an experiement in an automated fashion. This may include Dockerfiles, C programs, Python Programs, etc.. The experiment will be invoked by a Python program in the Scripts folder.

1) Dockerfile -> Compiles read.c into an image for running
2) read.c <number of trials> <size of read> -> The driver program for this test. Will do the size of the read for x number of trials and average out the time taken to do this. Usually, the number of trials is very high, say 10000. Expects a file atleast as large as the size of read in bytes given called "file.txt". Generate this in the python script.
3) read: Binary of read.c
4) file.txt -> 10 MB file of random bytes for reading by the program
