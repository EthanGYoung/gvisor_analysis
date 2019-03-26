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
			results[row[0]] = {}
		if (row[1] not in results[row[0]]):
			results[row[0]][row[1]] = []
				
		results[row[0]][row[1]].append(float(row[2]))

# Calculate mean throughput for each
def throughput(data):
	return (data *1000000) # Microsec

averages = {}
for platform in results:
	if (platform not in averages):
		averages[platform] = {}

	for size in results[platform]:
		averages[platform][size] = throughput(statistics.mean(results[platform][size]))

# Sort keys inorder of size
def sort_keys(mydict):
        mylist = []

        keylist = sorted(mydict.keys(), key=int)
        for key in keylist:
                mylist.append(mydict[key])
        return mylist

for platform in averages:
		averages[platform] = sort_keys(averages[platform])

plt.rc('font', family='serif')
plt.rc('xtick', labelsize='x-small')
plt.rc('ytick', labelsize='x-small')
fig = plt.figure(figsize=(3.5, 2.5))
ax = fig.add_subplot(1, 1, 1)
n_groups = 4

print(averages)
# create plot
index = np.arange(n_groups)
bar_width = 0.3
opacity = 0.8

rects1 = plt.bar(index, averages['getuid'], bar_width,
alpha=opacity,
color='0.1',
label='getuid')

rects2 = plt.bar(index + 1*bar_width, averages['gid'], bar_width,
alpha=opacity,
color='0.6',
label='getgid')

'''	
rects3 = plt.bar(index +  2*bar_width, averages['runsc_ptrace'], bar_width,
alpha=opacity,
color='0.6',
label='runsc_ptrace')

rects3 = plt.bar(index + 3*bar_width, averages['runsc_kvm'], bar_width,
alpha=opacity,
color='0.8',
label='runsc_kvm')
'''
plt.ylabel('Time (Microseconds)', fontsize=10)
plt.xticks(index + 1*bar_width, ("bare", "runc", "ptrace", "kvm"))
plt.xlim(left=-1*bar_width)
plt.legend(loc = 'upper left')
plt.legend(loc = 'upper left', frameon=False, prop={'size':10})
ax.tick_params(axis=u'both', which=u'both',length=0)	 
plt.tight_layout()
plt.savefig('./systemcall_time.eps', format='eps', dpi=1000)
plt.show()
