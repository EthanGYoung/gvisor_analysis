import json
from subprocess import Popen

''' -----------Methods-------------------'''

def handleConfig():
	print("")
	print("Printing config.json")
	
	with open("config.json") as f:
		data = json.load(f)
	
	# print config
	print(data)
	print("")

	return data

def printExperimentsOverview():
	print("Running all experiments specified in config.py") 

def runExperiments(config):
	for exp in config["experiments"]:
		for name in exp:
			print("")
			if (exp[name] == "False"):
				print("Not running " + str(name) + " due to config specification")
				continue

			print("Running experiment: " + str(name))

			p = Popen(['/bin/bash', '-c', "python " + str(name) + "/scripts/run.py"])  
			p.wait()

''' ---------------Executed Code---------------'''
EXP_NUM = 1

print("Running automated experiments")

# Print config file
config = handleConfig()

# Print experiment overview
printExperimentsOverview()

print("")
print("Beginning execution")
print("")

runExperiments(config)

