import numpy as np
import statistics
import sys
import matplotlib.pyplot as plt
import csv
import math

results = {}

# Grab data and put into dictionary
with open(sys.argv[1]) as f:
	csv_reader = csv.reader(f, delimiter=',')
	for row in csv_reader:
		if (row[0] not in results):
			results[row[0]] = []
				
		results[row[0]].append(float(row[2]))

# Calculate mean throughput (1000 Calls/second) for each
def throughput(data, control):
	return control/(data) # 1 second 

averages = {}
for platform in results:
	averages[platform] = throughput(statistics.mean(results[platform]), statistics.mean(results["runsc_kvm"]))

# Sort keys inorder of size
def sort_keys(mydict):
        mylist = []

        keylist = sorted(mydict.keys(), key=int)
        for key in keylist:
                mylist.append(mydict[key])
        return mylist

print(averages)

n_groups = 1

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.05
opacity = 0.8
x = []

for i in range(0, len(averages)):
	x.append(index+bar_width*i)	

rects1 = plt.bar(x[0], averages['bare'], bar_width/2,
alpha=opacity,
color='0.2',
label='bare')

rects2 = plt.bar(x[1], averages['runc'], bar_width/2,
alpha=opacity,
color='0.5',
label='runc')

rects4 = plt.bar(x[3], averages['runsc_kvm'], bar_width/2,
alpha=opacity,
hatch='/',
color='0.8',
label='runsc_kvm')

plt.ylabel('Ratio Open/Close Time Relative to Runsc_kvm')
plt.title('Time of Open/Close System Call Relative to Runsc_kvm')
for i in range(0, len(averages)):
	x[i] = x[i] +  bar_width/4
plt.xticks(x,["bare","runc","runsc_kvm"])
plt.xlim(left=0)
#plt.legend(loc = 'upper right')
 
plt.tight_layout()
plt.show()

