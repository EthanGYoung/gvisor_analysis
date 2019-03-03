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

for i in range(0, len(averages)-2):
	x.append(index+bar_width*i)	

rects1 = plt.bar(x[3], averages['bare'], bar_width/2,
alpha=opacity,
color='0.3',
label='bare')

rects2 = plt.bar(x[2], averages['runc'], bar_width/2,
hatch='-',
alpha=opacity,
color='0.5',
label='runc')
'''
rects3 = plt.bar(x[1], averages['runsc_ptrace'], bar_width/2,
alpha=opacity,
color='0.7',
label='runsc_ptrace')
'''
rects4 = plt.bar(x[0], averages['runsc_kvm'], bar_width/2,
alpha=opacity,
hatch='/',
color='0.9',
label='runsc_kvm')

'''
rects5 = plt.bar(x[4], averages['mod_ptrace'], bar_width/2,
alpha=opacity,
color='r',
label='mod_ptrace')
'''
rects6 = plt.bar(x[1], averages['mod_kvm'], bar_width/2,
alpha=opacity,
color='b',
label='mod_kvm')

plt.ylabel('Ratio Open/Close Time Relative to Runsc_kvm')
plt.title('Time of Open/Close System Call Relative to Runsc_kvm')
for i in range(0, len(averages)-2):
	x[i] = x[i] +  bar_width/4
plt.xticks(x,["runc_kvm","kvm_mod","runc","bare"])
plt.xlim(left=0)
#plt.legend(loc = 'upper right')
 
plt.tight_layout()
plt.show()

