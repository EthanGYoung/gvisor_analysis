from subprocess import Popen

if (len(sys.argv) < 2):
        print("Incorrect args. Did you pass a path?")
        return

path = sys.argv[1]

# Builds any images or binaries in the experiment_materials folder
print("Deleting old image for no_op")
p = Popen(['/bin/bash', '-c', 'docker image rm no_op'])
p.wait()

print("Building Docker image for no_op")
p = Popen(['/bin/bash', '-c', 'docker build -t no_op " + str(path) + "/experiment_materials/'])
p.wait()

print("Building C executable spinup")
p = Popen(['/bin/bash', '-c' , 'gcc -pthread -o " + str(path) + "/experiment_materials/spinup -std=gnu99 " + str(path) + "/experiment_materials/spinup.c'])
p.wait()
