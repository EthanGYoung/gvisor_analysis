from subprocess import Popen

# Builds any images or binaries in the experiment_materials folder
print("Building Docker image for write")
p = Popen(['/bin/bash', '-c', 'docker build -t write 2_exp/experiment_materials/'])
p.wait()

print("Building C executable write")
p = Popen(['/bin/bash', '-c' , 'gcc -o 2_exp/experiment_materials/write -std=gnu99 2_exp/experiment_materials/write.c'])
p.wait()
