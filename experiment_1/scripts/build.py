from subprocess import Popen

# Builds any images or binaries in the experiment_materials folder
p = Popen(['/bin/bash', '-c', 'docker build -t read ../experiment_materials/'])
p.wait()
