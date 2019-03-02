import numpy as np
import statistics
import sys
import matplotlib.pyplot as plt
import csv

results = {}

# Grab data and put into dictionary
with open(sys.argv[1]) as f:
	csv_reader = csv.reader(f, delimiter=',')
	for row in csv_reader:
		if (row[0] not in results):
			results[row[0]] = []
				
		results[row[0]].append(float(row[2]))

# Calculate mean throughput (1000 Calls/second) for each
def throughput(data):
	return 1/(data*1000) # 1 second 

averages = {}
for platform in results:
	averages[platform] = throughput(statistics.mean(results[platform]))

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
bar_width = 0.1
opacity = 0.8

rects1 = plt.bar(index, averages['bare'], bar_width,
alpha=opacity,
color='0.3',
label='bare')

rects2 = plt.bar(index + 1*bar_width, averages['runc'], bar_width,
hatch='-',
alpha=opacity,
color='0.5',
label='runc')

rects3 = plt.bar(index +  2*bar_width, averages['runsc_ptrace'], bar_width,
alpha=opacity,
color='0.7',
label='runsc_ptrace')

rects4 = plt.bar(index + 3*bar_width, averages['runsc_kvm'], bar_width,
alpha=opacity,
hatch='/',
color='0.9',
label='runsc_kvm')

rects5 = plt.bar(index + 4*bar_width, averages['mod_ptrace'], bar_width,
alpha=opacity,
color='r',
label='mod_ptrace')

rects6 = plt.bar(index + 5*bar_width, averages['mod_kvm'], bar_width,
alpha=opacity,
color='b',
label='mod_kvm')

plt.ylabel('Average Throughput (1000 Calls/Sec)')
plt.title('Throughput of Open/Close System Calls')
plt.xticks([])
plt.ylim(top=700)

plt.legend(loc = 'upper right')
 
plt.tight_layout()
plt.show()

