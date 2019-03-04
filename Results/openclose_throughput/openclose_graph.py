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
	averages[platform] = statistics.mean(results[platform]) * 1000000 # Microseconds

# Sort keys inorder of size
def sort_keys(mydict):
        mylist = []

        keylist = sorted(mydict.keys(), key=int)
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

for i in range(0, len(averages)):
	x.append(index+bar_width*i)	
size_factor = 1.3
rects1 = plt.bar(x[0], averages['bare'], bar_width/size_factor,
edgecolor='0.5',
alpha=opacity,
color='0.5',
label='bare')

rects2 = plt.bar(x[3]+bar_width/size_factor, averages['tmpfs_bare'], bar_width/size_factor,
alpha=opacity,
edgecolor='0.5',
color='0.5',
label='tmpfs_bare')

rects3 = plt.bar(x[1], averages['runc'], bar_width/size_factor,
alpha=opacity,
edgecolor='0.5',
color='0.5',
label='runc')

rects4 = plt.bar(x[4]+bar_width/size_factor, averages['tmpfs_runc'], bar_width/size_factor,
alpha=opacity,
edgecolor='0.5',
color='0.5',
label='tmpfs_runc')

rects5 = plt.bar(x[2], averages['runsc_kvm'], bar_width/size_factor,
alpha=opacity,
edgecolor='0.5',
color='0.5',
label='runsc_kvm')

rects6 = plt.bar(x[5]+bar_width/size_factor, averages['tmpfs_runsc_kvm'], bar_width/size_factor,
alpha=opacity,
color='0.5',
edgecolor='0.5',
label='tmpfs_runsc_kvm')


plt.ylabel('Openclose System Call Time (Microseconds)')
plt.title('Time of Openclose System Call Using Different Runtimes and tmpfs')
for i in range(0, len(averages)/2):
	x[i] = x[i] + bar_width/size_factor/2
for i in range(len(averages)/2, len(averages)):
	x[i] = x[i] + bar_width/size_factor	#x[i] = x[i] +  bar_width/size_factor*1.5
plt.xticks(x,["bare","runc","runsc","tmpfs_bare","tmpfs_runsc", "tmpfs_runsc"])
plt.xlim(left=-bar_width/6)
plt.xticks(rotation=30)
#plt.legend(loc = 'upper right')
#ax.yaxis.grid(True) 
plt.tight_layout()
plt.savefig('./openclose_time.eps', format='eps', dpi=1000)
plt.show()
