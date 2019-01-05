import os
import json
from subprocess import Popen

''' -----------Methods-------------------'''

def handleConfig():
	print("")
	print("Printing config.txt")
	
	with open("4_exp/scripts/config.json") as f:
		data = json.load(f)
	
	# print config
	print(data)
	print("")

	return data

def printExperimentOverview(TRIALS):
	print("Testing network throughput for " + TRIALS + " trials.") 

def runExperiment(TRIALS, config):
	print("")
	print("Running baremetal")
	for names in config["URLS"]:
		for url in names:
			print("Running exp: 4_exp/experiment_materials/net " + str(TRIALS) + " " + str(names[url]))
			p = Popen(['/bin/bash', '-c',  "4_exp/experiment_materials/net " + str(TRIALS) + " " +  str(names[url])])
			p.wait()

	print("")
	print("Running with Docker")
		
	runDockerContainer("--runtime=runc", TRIALS, config)
	
	print("")
	print("Running gVisor: Ptrace")
	
	modifyDockerConfig("ptrace")
	runDockerContainer("--runtime=runsc", TRIALS, config)
	
	print("")
	print("Running gVisor: KVM")
	
	modifyDockerConfig("kvm")
	runDockerContainer("--runtime=runsc", TRIALS, config)


	print("Completed experiment " + str(EXP_NUM))

# runtime = "" if no runsc, else --runtime=runsc
def runDockerContainer(runtime, TRIALS, config):
	for names in config["URLS"]:
		for url in names:
			print("Running exp: sudo docker run " + str(runtime) + " --rm net " + str(TRIALS) + " " + str(names[url]))
			p = Popen(['/bin/bash', '-c',  "docker run " + str(runtime) + " --rm net " + str(TRIALS) + " " +  str(names[url])])
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
EXP_NUM = 4

print("Running experiment " + str(EXP_NUM))
print(os.getcwd())

# Print config file
config = handleConfig()

TRIALS = config["trials"]

if (config["built"] != "True"):
	print("Building experiment")
	p = Popen(['/bin/bash', '-c', 'python 4_exp/scripts/build.py'])
	p.wait()
else:
	print("Experiment already built")

# Print experiment overview
printExperimentOverview(TRIALS)

print("")
print("Beginning experiment_" + str(EXP_NUM))
print("")

runExperiment(TRIALS, config)

