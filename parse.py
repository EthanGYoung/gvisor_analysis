#Average for 1000 calls: getpid syscall time = 0.000000014086 seconds
import os
import sys

def present(words, string):
	for word in words:	
		if word in string:
			return True
	
	return False

FILE_PATH = str(sys.argv[1])
INDICATORS = sys.argv[2:]

#print("Parsing log file in " + str(FILE_PATH))
#print("Indicators are " + str(INDICATORS))

for filename in os.listdir(FILE_PATH):
	with open(FILE_PATH + filename, "r") as f:
		print("Parsing log file: " + str(FILE_PATH + filename))
		for line in f:
			if (present(INDICATORS, line)):
				print(line.split('\n')[0])
		print("")

