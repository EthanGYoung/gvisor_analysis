from subprocess import Popen
import sys

if (len(sys.argv) < 2):
	print("Incorrect agrs. Are you passing path?")
	return

path = sys.argv[1]

print("Deleting old image for write")
p = Popen(['/bin/bash', '-c', 'docker image rm write'])
p.wait()

# Builds any images or binaries in the experiment_materials folder
print("Building Docker image for write")
p = Popen(['/bin/bash', '-c', 'docker build -t write " + str(path) + "/experiment_materials/'])
p.wait()

print("Building C executable write")
p = Popen(['/bin/bash', '-c' , 'gcc -o " + str(path) + "/experiment_materials/write -std=gnu99 " + str(path) + "/experiment_materials/write.c'])
p.wait()
