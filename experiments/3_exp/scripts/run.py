import os
import sys
import json
from subprocess import Popen

''' -----------Methods-------------------'''
def flush():
        sys.stdout.flush()
        sys.stderr.flush()

def handleConfig(path):
	print("")
	print("Printing config.txt")
	
	with open(str(path) + "/scripts/config.json") as f:
		data = json.load(f)
	
	# print config
	print(data)
	print("")

	return data

def printExperimentOverview(TRIALS, NUM_THREADS, NUM_SPINUPS):
	print("Testing spinup throughput for " + TRIALS + " trials. Cycling from 1 to " + str(NUM_THREADS) + " threads used for spinning up " + str(NUM_SPINUPS) + " containers.") 

def runExperiment(TRIALS, NUM_THREADS, NUM_SPINUPS, path):
	print("")
	print("Running with Docker")
		
	runDockerContainer("--runtime=runc", NUM_THREADS, TRIALS, NUM_SPINUPS, path)
	
	print("")
	print("Running gVisor: Ptrace")
	
	modifyDockerConfig("ptrace")
	runDockerContainer("--runtime=runsc", NUM_THREADS, TRIALS, NUM_SPINUPS, path)
	
	print("")
	print("Running gVisor: KVM")
	
	modifyDockerConfig("kvm")
	runDockerContainer("--runtime=runsc", NUM_THREADS, TRIALS, NUM_SPINUPS, path)


	print("Completed experiment " + str(EXP_NUM))

# runtime = "" if no runsc, else --runtime=runsc
def runDockerContainer(runtime, NUM_THREADS, TRIALS, NUM_SPINUPS, path):
	flush()
	p = Popen(['/bin/bash', '-c', str(path) + "/experiment_materials/spinup " + str(NUM_THREADS) + " " + str(TRIALS) + " " + str(runtime) + " " + str(NUM_SPINUPS)])
	p.wait()
	flush()

def modifyDockerConfig(platform):
	print("Modifying docker daemon file")
	with open("/etc/docker/daemon.json") as f:
		data = json.load(f)
	data["runtimes"]["runsc"]["runtimeArgs"] = ["--platform=" + str(platform)]
	print("Writing: " + str(data))
	with open('/etc/docker/daemon.json', 'w') as outfile:
    		json.dump(data, outfile)

	print("Restarting Docker")
	flush()
	p = Popen(['/bin/bash', '-c',  "systemctl restart docker"])
	p.wait()
	p = Popen(['/bin/bash', '-c',  "systemctl status docker"])
	p.wait()
	flush()

''' ---------------Executed Code---------------'''
EXP_NUM = 3

print("Running experiment " + str(EXP_NUM))
print(os.getcwd())

if (len(sys.argv) < 2):
	print("Incorrect args. Did you pass a path?")
	return

path = sys.argv[1]

# Print config file
config = handleConfig(path)

TRIALS = config["trials"]
NUM_THREADS = config["num_threads"]
NUM_SPINUPS = config["num_spinups"]

if (config["built"] != "True"):
	print("Building experiment")
	flush()
	p = Popen(['/bin/bash', '-c', 'python ' + str(path) + '/scripts/build.py ' + str(path)])
	p.wait()
	flush()
else:
	print("Experiment already built")

# Print experiment overview
printExperimentOverview(TRIALS, NUM_THREADS, NUM_SPINUPS)

print("")
print("Beginning experiment_" + str(EXP_NUM))
print("")

runExperiment(TRIALS, NUM_THREADS, NUM_SPINUPS, path)

