# Materials

This folder is meant to hold all materials needed to run an experiement in an automated fashion. This may include Dockerfiles, C programs, Python Programs, etc.. The experiment will be invoked by a Python program in the Scripts folder.

1) Dockerfile -> Compiles net.c into an image for running
2) net.c "number of trials" "URL" -> The driver program for this test. Will do X trials of curl on the URL.
3) net: Binary of net.c
