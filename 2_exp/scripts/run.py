import os
import json
from subprocess import Popen

''' -----------Methods-------------------'''

def handleConfig():
	print("")
	print("Printing config.txt")
	
	with open("2_exp/scripts/config.json") as f:
		data = json.load(f)
	
	# print config
	print(data)
	print("")

	return data

def printExperimentOverview(TRIALS, WRITE_SIZE):
	print("Testing write throughput for " + TRIALS + " trials. Cycling from 1 to " + str(WRITE_SIZE) + " bytes of writeing.") 

def runExperiment(TRIALS, WRITE_SIZE):
	# Begin invoking experiment (Does 10 experiments for each config)
	
	
	print("")
	print("Running baremetal")
	for i in range(0, 10):
		exp_write = (int(WRITE_SIZE))*(10 - i)/10

		print("Running exp " + str(i+1) + " of 10: 2_exp/experiment_materials/write " + str(TRIALS) + " " + str(exp_write))
		p = Popen(['/bin/bash', '-c',  "2_exp/experiment_materials/write " + str(TRIALS) + " " +  str(exp_write)])
		p.wait()

	print("")
	print("Running with Docker")
		
	runDockerContainer("", WRITE_SIZE, TRIALS)
	
	print("")
	print("Running gVisor: Ptrace")
	
	modifyDockerConfig("ptrace")
	runDockerContainer("--runtime=runsc", WRITE_SIZE, TRIALS)
	
	print("")
	print("Running gVisor: KVM")
	
	modifyDockerConfig("kvm")
	runDockerContainer("--runtime=runsc", WRITE_SIZE, TRIALS)


	print("Completed experiment " + str(EXP_NUM))

# runtime = "" if no runsc, else --runtime=runsc
def runDockerContainer(runtime, WRITE_SIZE, TRIALS):
	for i in range(0, 10):
		exp_write = (int(WRITE_SIZE))*(10 - i)/10

		print("Running exp " + str(i+1) + " of 10: sudo docker run " + str(runtime) + " --rm write " + str(TRIALS) + " " + str(exp_write))
		p = Popen(['/bin/bash', '-c',  "docker run " + str(runtime) + " --rm write " + str(TRIALS) + " " +  str(exp_write)])
		p.wait()

def modifyDockerConfig(platform):
	print("Modifying docker daemon file")
	with open("/etc/docker/daemon.json") as f:
		data = json.load(f)
	data["runtimes"]["runsc"]["runtimeArgs"] = ["--platform=" + str(platform)]
	print("Writing: " + str(data))
	with open('/etc/docker/daemon.json', 'w') as outfile:
    		json.dump(data, outfile)

	print("Restarting Docker")
	p = Popen(['/bin/bash', '-c',  "systemctl restart docker"])
	p.wait()
	p = Popen(['/bin/bash', '-c',  "systemctl status docker"])
	p.wait()

''' ---------------Executed Code---------------'''
EXP_NUM = 2

print("Running experiment " + str(EXP_NUM))
print(os.getcwd())

# Print config file
config = handleConfig()

TRIALS = config["trials"]
WRITE_SIZE = config["write_size"]

if (config["built"] != "True"):
	print("Building experiment")
	p = Popen(['/bin/bash', '-c', 'python 2_exp/scripts/build.py'])
	p.wait()
else:
	print("Experiment already built")

# Print experiment overview
printExperimentOverview(TRIALS, WRITE_SIZE)

print("")
print("Beginning experiment_" + str(EXP_NUM))
print("")

runExperiment(TRIALS, WRITE_SIZE)

