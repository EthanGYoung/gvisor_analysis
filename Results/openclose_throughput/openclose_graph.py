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
plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')
fig = plt.figure(figsize=(3.5, 2.5))
ax = fig.add_subplot(1, 1, 1)
index = np.arange(n_groups)
bar_width = 0.05
opacity = 0.8
x = []
plt.rcParams["figure.figsize"] = [3.5,2]
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
ax.text(0.104+bar_width/(size_factor*2)-0.015,40,'28.4',fontsize=10) #tmpfs_kvm
ax.text(0.154+bar_width/(size_factor*2)-0.015,525,'518',fontsize=10) #vol_kvm

#Time
ax.text(0+bar_width/(size_factor*2)-0.005,20,'2.04',fontsize=10) #tmpfs_bare
ax.text(0.05+bar_width/(size_factor*2)-0.005,20,'2.40',fontsize=10) #tmpfs_runc
plt.ylabel(u'Time (microsec)')
for i in range(0,4):
	x[i] = x[i] + bar_width/(size_factor*2)
plt.xticks(x,["bare","runc","internal","external"])
plt.xlim(left=-bar_width/6)
#plt.legend(loc = 'upper right')
ax.tick_params(axis=u'both', which=u'both',length=0)
#ax.yaxis.grid(True) 
plt.tight_layout()
plt.savefig('./openclose_time.eps', format='eps', dpi=1000)
plt.show()
