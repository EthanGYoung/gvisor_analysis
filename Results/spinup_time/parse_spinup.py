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
		if ('\xef\xbb\xbf' in row[0]):
			continue
		if (row[0] not in results):
			print(row)
			results[row[0]] = []

		results[row[0]].append(float(row[2]))

averages = {}
for platform in results:
	averages[platform] = statistics.mean(results[platform])

# Sort keys inorder of size
def sort_keys(mydict):
        mylist = []

        keylist = sorted(mydict.keys())
        for key in keylist:
                mylist.append(mydict[key])
        return mylist

n_groups = 1

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.05
opacity = 0.8
x = []
print(averages)
for i in range(0, len(averages)):
	x.append(index+bar_width*i)
size_factor = 2
rects1 = plt.bar(x[0]+bar_width/size_factor * 0.5, averages['runc'], bar_width/size_factor,
alpha=opacity,
color='0.3',
label='runc')

rects2 = plt.bar(x[0]+bar_width/size_factor*1.5, averages['runc_tmpfs'], bar_width/size_factor,
alpha=opacity,
color='0.5',
label='runc_tmpfs')

rects3 = plt.bar(x[3]-bar_width/size_factor * 1.5, averages['runsc_kvm'], bar_width/size_factor,
alpha=opacity,
color='0.7',
label='runsc_kvm')

rects4 = plt.bar(x[3] - bar_width/size_factor *0.5, averages['runsc_kvm_tmpfs'], bar_width/size_factor,
alpha=opacity,
color='0.9',
label='runsc_kvm_tmpfs')

print(averages)
plt.ylabel('Container Spinup Time (ms)')
for i in range(0, int(len(averages)/2)):
	x[i] = x[i] +  bar_width/size_factor/2

for i in range(int(len(averages)/2), len(averages)):
	x[i] = x[i] +  bar_width/size_factor * 0.5
x[1] = x[1] - bar_width/size_factor
x[3] = x[2] + bar_width/size_factor

plt.xticks(x,["runc","runc_tmpfs","runsc_kvm","runsc_kvm_tmpfs"])
plt.xlim(left=-bar_width/4)
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig('./spinup_result.eps', format='eps', dpi=1000)
plt.show()
