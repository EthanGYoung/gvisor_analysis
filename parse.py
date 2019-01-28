#Average for 1000 calls: getpid syscall time = 0.000000014086 seconds
import os
import sys

if (len(sys.argv) != 2):
        print("Usage: python parse.py <app_log_dir_name>")

FILE_PATH = str(sys.argv[1])

print("Parsing log file in " + str(FILE_PATH))

with open(FILE_PATH, "r") as f:
    for line in f:
        if ("LOG_OUTPUT" in line):
                print(line.split('\n')[0])
