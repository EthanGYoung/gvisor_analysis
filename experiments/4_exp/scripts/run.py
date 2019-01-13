import sys
import os
import json
from subprocess import Popen

''' -----------Methods-------------------'''

def handleConfig(path):
	print("")
	print("Printing config.txt")
	
	with open(str(path) + "/scripts/config.json") as f:
		data = json.load(f)
	
	# print config
	print(data)
	print("")

	return data

def printExperimentOverview(TRIALS):
	print("Testing network throughput for " + TRIALS + " trials.") 

def runExperiment(TRIALS, config, path, log):
	print("")
	print("Running baremetal")
	for names in config["URLS"]:
		for url in names:
			print("Running exp: " + str(path) + "/experiment_materials/net " + str(TRIALS) + " " + str(names[url]))
			p = Popen(['/bin/bash', '-c',  str(path) + "/experiment_materials/net " + str(TRIALS) + " " +  str(names[url])], stdout = log, stderr = log)
			p.wait()

	print("")
	print("Running with Docker")
		
	runDockerContainer("--runtime=runc", TRIALS, config, path, log)
	
	print("")
	print("Running gVisor: Ptrace")
	
	modifyDockerConfig("ptrace")
	runDockerContainer("--runtime=runsc", TRIALS, config, path, log)
	
	print("")
	print("Running gVisor: KVM")
	
	modifyDockerConfig("kvm")
	runDockerContainer("--runtime=runsc", TRIALS, config, path, log)


	print("Completed experiment " + str(EXP_NUM))

# runtime = "" if no runsc, else --runtime=runsc
def runDockerContainer(runtime, TRIALS, config, path, log):
	for names in config["URLS"]:
		for url in names:
			flush()
			print("Running exp: sudo docker run " + str(runtime) + " --rm net " + str(TRIALS) + " " + str(names[url]))
			p = Popen(['/bin/bash', '-c',  "docker run " + str(runtime) + " --rm net " + str(TRIALS) + " " +  str(names[url])], stdout = log, stderr = log)
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
	p = Popen(['/bin/bash', '-c',  "systemctl restart docker"])
	p.wait()
	p = Popen(['/bin/bash', '-c',  "systemctl status docker"])
	p.wait()

''' ---------------Executed Code---------------'''
EXP_NUM = 4

print("Running experiment " + str(EXP_NUM))
print(os.getcwd())

if (len(sys.argv) < 3):
        print("Incorrect args. Did you pass a path or log?")

path = sys.argv[1]
log = open(str(sys.argv[2]), "a+")

# Print config file
config = handleConfig(path)

TRIALS = config["trials"]

if (config["built"] != "True"):
	print("Building experiment")
	p = Popen(['/bin/bash', '-c', 'python ' + str(path) + '/scripts/build.py ' + str(path) + " " + str(sys.argv[2])], stdout = log, stderr = log)
	p.wait()
else:
	print("Experiment already built")

# Print experiment overview
printExperimentOverview(TRIALS)

print("")
print("Beginning experiment_" + str(EXP_NUM))
print("")

runExperiment(TRIALS, config, path, log)

