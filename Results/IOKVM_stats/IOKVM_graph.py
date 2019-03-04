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

averages = {}
for platform in results:
	if (platform not in averages):
		averages[platform] = {}

	for size in results[platform]:
		averages[platform][size] = statistics.mean(results[platform][size])

# Sort keys inorder of size
def sort_keys(mydict):
        mylist = []

        keylist = sorted(mydict.keys(), key=int)
        for key in keylist:
                mylist.append(mydict[key])
        return mylist

for platform in averages:
		averages[platform] = sort_keys(averages[platform])
print(averages)
if (sys.argv[2] == "bar"):
	n_groups = 2

	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.1
	opacity = 0.8
	
	rects1 = plt.bar(index, averages['runsc_kvm_exit'], bar_width,
	hatch='/',
	alpha=opacity,
	color='0.2',
	label='kvm_exit')

	rects2 = plt.bar(index + 1*bar_width, averages['runsc_tmpfs_kvm_exit'], bar_width,
	hatch='-',
	alpha=opacity,
	color='0.5',
	label='tmpfs_kvm_exit')
	

	rects3 = plt.bar(index + 2*bar_width, averages['runsc_kvm_userspace'], bar_width,
	alpha=opacity,
	color='0.8',
	label='kvm_userspace_exit')
	
	rects4 = plt.bar(index + 3*bar_width, averages['runsc_tmpfs_kvm_userspace'], bar_width,
	hatch='.',
	alpha=opacity,
	color='0.8',
	label='tmpfs_kvm_userspace_exit')

	plt.xlabel('Size of Read')
	plt.ylabel('Number of Calls')
	plt.title('Number of kvm_exits and kvm_userspace_exits With And Without tmpfs')
	plt.xticks(index + 2*bar_width, ("4KB", "1MB"))
	plt.xlim(left=-2*bar_width)
	plt.legend(loc = 'upper left')
	 
	plt.tight_layout()
#	plt.savefig('./network_throughput.eps', format='eps', dpi=1000)
plt.show()
