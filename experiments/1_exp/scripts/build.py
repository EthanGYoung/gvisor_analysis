from subprocess import Popen
import sys

if (len(sys.argv) < 3):
	print("Incorrect arguments for build.py. Probably missing path or log")

path = sys.argv[1]
log = open(str(sys.argv[2]), "a+")


# Builds any images or binaries in the experiment_materials folder
print("Deleting old image for read")
p = Popen(["/bin/bash", "-c", "docker image rm read"], STDOUT = log, STDERR = log)
p.wait()

print("Building Docker image for read")
p = Popen(["/bin/bash", "-c", "docker build -t read " + str(path) + "/experiment_materials/"], STDOUT = log, STDERR = log)
p.wait()

print("Building C executable read")
p = Popen(["/bin/bash", "-c" , "gcc -o " + str(path) + "/experiment_materials/read -std=gnu99 " + str(path) + "/experiment_materials/read.c", STDOUT = log, STDERR = log])
p.wait()
