from subprocess import Popen
import sys

if (len(sys.argv) < 3):
        print("Incorrect args. Did you pass a path or log?")

path = sys.argv[1]
log = open(str(sys.argv[2]), "a+")

# Builds any images or binaries in the experiment_materials folder
print("Deleting old image for no_op")
p = Popen(["/bin/bash", "-c", "docker image rm --force no_op"], stdout = log, stderr = log)
p.wait()

print("Building Docker image for no_op")
p = Popen(["/bin/bash", "-c", "docker build -t no_op " + str(path) + "/experiment_materials/"], stdout = log, stderr = log)
p.wait()

print("Building C executable spinup")
p = Popen(["/bin/bash", "-c" , "gcc -pthread -o " + str(path) + "/experiment_materials/spinup -std=gnu99 " + str(path) + "/experiment_materials/spinup.c"], stdout = log, stderr = log)
p.wait()
