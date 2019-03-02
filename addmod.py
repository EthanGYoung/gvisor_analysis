import sys

infile = sys.argv[1]
outfile = sys.argv[2]

with open(infile, "r") as in_f:
	with open(outfile, "a+") as out_f:
		for line in in_f:
			out_f.write(line.rstrip('\n') + " mod\n")	
