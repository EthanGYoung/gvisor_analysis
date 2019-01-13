from subprocess import Popen
import sys

if (len(sys.argv) < 3):
	print("Incorrect agrs. Are you passing path and log?")

path = sys.argv[1]
log = open(str(sys.argv[2]), "a+")

print("Deleting old image for write")
p = Popen(["/bin/bash", "-c", "docker image rm write"], stdout = log, stderr = log)
p.wait()

# Builds any images or binaries in the experiment_materials folder
print("Building Docker image for write")
p = Popen(["/bin/bash", "-c", "docker build -t write " + str(path) + "/experiment_materials/"], stdout = log, stderr = log)
p.wait()

print("Building C executable write")
p = Popen(["/bin/bash", "-c" , "gcc -o " + str(path) + "/experiment_materials/write -std=gnu99 " + str(path) + "/experiment_materials/write.c"], stdout = log, stderr = log)
p.wait()
