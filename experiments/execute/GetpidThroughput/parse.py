#Average for 1000 calls: getpid syscall time = 0.000000014086 seconds
import os
import sys

if (len(sys.argv) != 2):
	print("Incorrect args for parse.py")
	
TEST_DIR = str(sys.argv[1])
LOG_PATH = "/logs/test.log"

FILE_PATH = TEST_DIR + LOG_PATH
print("Parsing log file in " + str(FILE_PATH))

with open(FILE_PATH, "r") as f:
    for line in f:
	if ("getpid syscall time" in line):
		print(line.split('\n')[0])
