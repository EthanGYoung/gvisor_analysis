from subprocess import Popen

# Builds any images or binaries in the experiment_materials folder
print("Building Docker image for read")
p = Popen(['/bin/bash', '-c', 'docker build -t read 1_exp/experiment_materials/'])
p.wait()

print("Building C executable read")
p = Popen(['/bin/bash', '-c' , 'gcc -o 1_exp/experiment_materials/read -std=gnu99 1_exp/experiment_materials/read.c'])
p.wait()
