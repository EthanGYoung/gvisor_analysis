import sys
import os
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

#def redirectToLog(config):
	#if (config["log"] != ""):
		# Delete existing file first
		#if os.path.exists(config["log"]):
  		#	os.remove(config["log"])

		# Redirects output to log file
		#f = open(config["log"], "w")
		#sys.stderr = f
		#sys.stdout = f

def runExperiments(config):
	for exp in config["experiments"]:
		for name in exp:
			print("")
			if (exp[name] == "False"):
				print("Not running " + str(name) + " due to config specification")
				continue

			print("Running experiment: " + str(name))
			sys.stdout.flush()
		#	if (config["log"] != ""):
		#		p = Popen(['/bin/bash', '-c', "python " + str(name) + "/scripts/run.py 2>&1 >> " + config["log"]])  
		#	else:
			p = Popen(['/bin/bash', '-c', "python " + str(name) + "/scripts/run.py" ])  
			p.wait()

''' ---------------Executed Code---------------'''

print("Running automated experiments")

# Print config file
config = handleConfig()

# Print experiment overview
printExperimentsOverview()

print("")
print("Beginning execution")
print("")

# Redirect stdout and stderr
#redirectToLog(config)

runExperiments(config)

