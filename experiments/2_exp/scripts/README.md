# Scripts

1) run.py -> runs read.c (in experiment materials) on bare metal, Docker (runc), Docker (runsc - ptrace), and Docker (runsc - kvm)
2) Build.py -> builds the image of read.c for docker and compiles read.c for the baremetal
3) Config.json -> Can specify the number of trials and the read size for the experiment
