# Materials

This folder is meant to hold all materials needed to run an experiement in an automated fashion. This may include Dockerfiles, C programs, Python Programs, etc.. The experiment will be invoked by a Python program in the Scripts folder.

1) Dockerfile -> creates a no-op image out of no_op.c
2) spinup.c -> driver program behind this experiment. Runs threads to spinup as many containers as possible.
3) no_op.c -> a no-op program that is just an empty container
