import sys

count=0

with open(sys.argv[2],'r') as f:
	for line in f:
		if sys.argv[1] in line:
			count += 1

print(count) 
