import os, sys, json
from subprocess import Popen

""" -----------Methods-------------------"""
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

def printExperimentOverview(TRIALS, NUM_CALLS):
	print("Testing getpid throughput for " + TRIALS + " trials. Making " + str(NUM_CALLS) + " calls per trial.")

def runExperiment(TRIALS, NUM_CALLS, path, log):
	# Begin invoking experiment (Does 10 experiments for each config)
	
	print("")
	print("Running baremetal")

	for i in range(0, TRIALS):
		print("Running exp " + str(i+1) + " of " + str(TRIALS) + ": " + str(path) + "/experiment_materials/getpid " + str(NUM_CALLS))
		flush()
		p = Popen(["/bin/bash", "-c",  str(path) + "/experiment_materials/getpid " + str(NUM_CALLS))], stdout = log, stderr = log)
		p.wait()
		flush()

	print("")
	print("Running with Docker")
		
	runDockerContainer("", NUM_CALLS, TRIALS, log)
	
	print("")
	print("Running gVisor: Ptrace")
	
	modifyDockerConfig("ptrace")
	runDockerContainer("--runtime=runsc", NUM_CALLS, TRIALS, log)
	
	print("")
	print("Running gVisor: KVM")
	
	modifyDockerConfig("kvm")
	runDockerContainer("--runtime=runsc", NUM_CALLS, TRIALS, log)


	print("Completed experiment " + str(EXP_NUM))

# runtime = "" if no runsc, else --runtime=runsc
def runDockerContainer(runtime, NUM_CALLS, TRIALS, log):
	for i in range(0, TRIALS):
		print("Running exp " + str(i+1) + " of 10: sudo docker run " + str(runtime) + " --rm getpid " + str(NUM_CALLS))
		flush()
		p = Popen(["/bin/bash", "-c",  "docker run " + str(runtime) + " --rm getpid " + str(TRIALS)], stdout = log, stderr = log)
		p.wait()
		flush()

def modifyDockerConfig(platform):
	print("Modifying docker daemon file")
	with open("/etc/docker/daemon.json") as f:
		data = json.load(f)
	data["runtimes"]["runsc"]["runtimeArgs"] = ["--platform=" + str(platform)]
	print("Writing: " + str(data))
	with open("/etc/docker/daemon.json", "w") as outfile:
    		json.dump(data, outfile)

	print("Restarting Docker")
	flush()
	p = Popen(["/bin/bash", "-c",  "systemctl restart docker"])
	p.wait()
	p = Popen(["/bin/bash", "-c",  "systemctl status docker"])
	p.wait()
	flush()

""" ---------------Executed Code---------------"""
EXP_NUM = 2

print("Running experiment " + str(EXP_NUM))
print(os.getcwd())

if (len(sys.argv) < 3):
	print("Incorrect args. Check if passing path")

path = sys.argv[1]
log = open(str(sys.argv[2]), "a+")

# Print config file
config = handleConfig(path)

TRIALS = config["trials"]
NUM_CALLS = config["num_calls"]

if (config["built"] != "True"):
	print("Building experiment")
	flush()
	p = Popen(["/bin/bash", "-c", "python " + str(path) + "/scripts/build.py " + str(path) + " " + str(sys.argv[2])], stdout = log, stderr = log)
	p.wait()
	flush()
else:
	print("Experiment already built")

# Print experiment overview
printExperimentOverview(TRIALS, NUM_CALLS)

print("")
print("Beginning experiment_" + str(EXP_NUM))
print("")

runExperiment(TRIALS, NUM_CALLS, path, log)

