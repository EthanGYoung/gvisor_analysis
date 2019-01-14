from subprocess import Popen
import sys

if (len(sys.argv) < 3):
	print("Incorrect agrs. Are you passing path and log?")

path = sys.argv[1]
log = open(str(sys.argv[2]), "a+")

print("Deleting old image for getpid")
p = Popen(["/bin/bash", "-c", "docker image rm getpid"], stdout = log, stderr = log)
p.wait()

# Builds any images or binaries in the experiment_materials folder
print("Building Docker image for getpid")
p = Popen(["/bin/bash", "-c", "docker build -t getpid " + str(path) + "/experiment_materials/"], stdout = log, stderr = log)
p.wait()

print("Building C executable getpid")
p = Popen(["/bin/bash", "-c" , "gcc -o " + str(path) + "/experiment_materials/getpid -std=gnu99 " + str(path) + "/experiment_materials/getpid.c"], stdout = log, stderr = log)
p.wait()
