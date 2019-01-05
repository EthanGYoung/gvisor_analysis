# Materials

This folder is meant to hold all materials needed to run an experiement in an automated fashion. This may include Dockerfiles, C programs, Python Programs, etc.. The experiment will be invoked by a Python program in the Scripts folder.

1) Dockerfile -> Compiles write.c into an image for running
2) write.c <number of trials> <size of write> -> The driver program for this test. Will do the size of the write for x number of trials and average out the time taken to do this. Usually, the number of trials is very high, say 10000.
3) write: Binary of write.c
