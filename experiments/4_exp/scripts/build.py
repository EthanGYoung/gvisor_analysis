from subprocess import Popen

if (len(sys.argv) < 2):
        print("Incorrect args. Did you pass a path?")
        return

path = sys.argv[1]

# Builds any images or binaries in the experiment_materials folder
print("Deleting old image for net")
p = Popen(['/bin/bash', '-c', 'docker image rm net'])
p.wait()

print("Building Docker image for net")
p = Popen(['/bin/bash', '-c', 'docker build -t net " + str(path) + "/experiment_materials/'])
p.wait()

print("Building C executable net")
p = Popen(['/bin/bash', '-c' , 'gcc -o " + str(path) + "/experiment_materials/net -std=gnu99 " + str(path) + "/experiment_materials/net.c'])
p.wait()
