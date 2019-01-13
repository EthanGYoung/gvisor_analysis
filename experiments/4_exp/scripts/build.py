from subprocess import Popen
import sys

if (len(sys.argv) < 3):
        print("Incorrect args. Did you pass a path?")

path = sys.argv[1]
log = open(str(sys.argv[2]), "a+")

# Builds any images or binaries in the experiment_materials folder
print("Deleting old image for net")
p = Popen(["/bin/bash", "-c", "docker image rm net"], stdout = log, stderr = log)
p.wait()

print("Building Docker image for net")
p = Popen(["/bin/bash", "-c", "docker build -t net " + str(path) + "/experiment_materials/"], stdout = log, stderr = log)
p.wait()

print("Building C executable net")
p = Popen(["/bin/bash", "-c" , "gcc -o " + str(path) + "/experiment_materials/net -std=gnu99 " + str(path) + "/experiment_materials/net.c"], stdout = log, stderr = log)
p.wait()
