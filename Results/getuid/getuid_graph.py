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

plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')
fig = plt.figure(figsize=(3.5, 2.5))
ax = fig.add_subplot(1, 1, 1)
# create plot
index = np.arange(n_groups)
bar_width = 0.05
opacity = 0.8
x = []

for i in range(0, len(averages)):
	x.append(index+bar_width*i)	
size_factor = 1.3
rects1 = plt.bar(x[0], averages['bare'], bar_width/size_factor,
edgecolor="0.5",
alpha=opacity,
color='0.5',
label='bare')

rects2 = plt.bar(x[1], averages['runc'], bar_width/size_factor,
edgecolor="0.5",
alpha=opacity,
color='0.5',
label='runc')

rects3 = plt.bar(x[2], averages['runsc_ptrace'], bar_width/size_factor,
edgecolor="0.5",
alpha=opacity,
color='0.5',
label='runsc_ptrace')

rects4 = plt.bar(x[3], averages['runsc_kvm'], bar_width/size_factor,
edgecolor="0.5",
alpha=opacity,
color='0.5',
label='runsc_kvm')

'''
rects5 = plt.bar(x[4], averages['mod_ptrace'], bar_width/2,
alpha=opacity,
color='r',
label='mod_ptrace')

rects6 = plt.bar(x[1], averages['mod_kvm'], bar_width/2,
alpha=opacity,
color='b',
label='mod_kvm')
'''
plt.ylabel('Getuid Time (Microseconds)', fontsize=10)
for i in range(0, len(averages)):
	x[i] = x[i] +  bar_width/size_factor/2

print(x)

plt.xticks(x,["bare","runc","ptrace","kvm"])
plt.xlim(left=-bar_width/6)
ax.tick_params(axis=u'both', which=u'both',length=0)
#plt.legend(loc = 'upper right')
#ax.yaxis.grid(True) 
plt.tight_layout()
plt.savefig('./getuid_time.eps', format='eps', dpi=1000)
plt.show()
