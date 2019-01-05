from subprocess import Popen

# Builds any images or binaries in the experiment_materials folder
print("Building Docker image for net")
p = Popen(['/bin/bash', '-c', 'docker build -t net 4_exp/experiment_materials/'])
p.wait()

print("Building C executable net")
p = Popen(['/bin/bash', '-c' , 'gcc -o 4_exp/experiment_materials/net -std=gnu99 4_exp/experiment_materials/net.c'])
p.wait()
