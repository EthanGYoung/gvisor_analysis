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

for i in range(0, 4):
	x.append(index+bar_width*i)	
size_factor = 1.3
rects1 = plt.bar(x[0], averages['tmpfs_bare'], bar_width/size_factor,
alpha=opacity,
edgecolor='0.5',
color='0.5',
label='tmpfs_bare')

rects2 = plt.bar(x[1], averages['tmpfs_runc'], bar_width/size_factor,
alpha=opacity,
edgecolor='0.5',
color='0.5',
label='tmpfs_runc')

rects3 = plt.bar(x[2], averages['tmpfs_runsc_kvm'], bar_width/size_factor,
alpha=opacity,
color='0.5',
edgecolor='0.5',
label='tmpfs_runsc_kvm')

rects4 = plt.bar(x[3], averages['vol_tmpfs_kvm'], bar_width/size_factor,
alpha=opacity,
edgecolor='0.5',
color='0.5',
label='vol_tmpfs_kvm')

print(averages)
print(x)
# Add text boxes (userspace_exit)
ax.text(0+bar_width/(size_factor*2)-0.015,50,'Exits: 46.00K') #tmpfs_bare
ax.text(0.05+bar_width/(size_factor*2)-0.015,50,'Exits: 37.00K') #tmpfs_runc
ax.text(0.1+bar_width/(size_factor*2)-0.015,40,'Exits: 19.00K') #tmpfs_kvm
ax.text(0.15+bar_width/(size_factor*2)-0.015,525,'Exits: 0.281K') #vol_kvm

#Time
ax.text(0+bar_width/(size_factor*2)-0.005,20,'2.04ms') #tmpfs_bare
ax.text(0.05+bar_width/(size_factor*2)-0.005,20,'2.40ms') #tmpfs_runc
'''
[array([ 0.]), array([ 0.05]), array([ 0.1]), array([ 0.15])]
{'tmpfs_runsc_kvm': 28.42259046, 'vol_tmpfs_kvm': 518.42740211, 'tmpfs_bare': 2.04492831, 'tmpfs_runc': 2.40981564, 'runc': 2.5179358900000004, 'bare': 2.11011235, 'runsc_kvm': 288.18599882999996}
'''

plt.ylabel('Openclose System Call Time (Microseconds)')
plt.title('Time of Openclose System Call Using Different Runtimes and tmpfs')
for i in range(0,4):
	x[i] = x[i] + bar_width/(size_factor*2)
plt.xticks(x,["tmpfs_bare","tmpfs_runc","tmpfs_runsc_kvm","vol_tmpfs_runsc"])
plt.xlim(left=-bar_width/6)
plt.xticks(rotation=30)
#plt.legend(loc = 'upper right')
#ax.yaxis.grid(True) 
plt.tight_layout()
plt.savefig('./openclose_time.eps', format='eps', dpi=1000)
plt.show()
