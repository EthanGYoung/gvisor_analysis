from subprocess import Popen

# Builds any images or binaries in the experiment_materials folder
print("Building Docker image for no_op")
p = Popen(['/bin/bash', '-c', 'docker build -t no_op 3_exp/experiment_materials/'])
p.wait()

print("Building C executable spinup")
p = Popen(['/bin/bash', '-c' , 'gcc -o 3_exp/experiment_materials/spinup -std=gnu99 3_exp/experiment_materials/spinup.c'])
p.wait()
