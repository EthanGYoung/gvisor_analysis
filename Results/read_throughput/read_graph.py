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
def throughput(data, size):
	return int(size)/(data *1000000000) # GB/s

averages = {}
for platform in results:
	if (platform not in averages):
		averages[platform] = {}

	for size in results[platform]:
		averages[platform][size] = throughput(statistics.mean(results[platform][size]), size)

# Sort keys inorder of size
def sort_keys(mydict):
        mylist = []

        keylist = sorted(mydict.keys(), key=int)
        for key in keylist:
                mylist.append(mydict[key])
        return mylist

for platform in averages:
		averages[platform] = sort_keys(averages[platform])

if (sys.argv[2] == "bar"):
	n_groups = 5
	print(averages)
	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.2
	opacity = 0.8
	plt.rcParams["figure.figsize"] = [3.5,2]	
	rects1 = plt.bar(index + 0*bar_width, averages['tmpfs_bare'], bar_width,
	edgecolor='0.8',
	color='0.8',
	alpha=opacity,
	label='tmpfs_bare')

	rects2 = plt.bar(index + 1*bar_width, averages['tmpfs_runc'], bar_width,
	edgecolor='0.6',
	color='0.6',
	alpha=opacity,
	label='tmpfs_runc')
	
	rect3 = plt.bar(index +  2*bar_width, averages['tmpfs_runsc_kvm'], bar_width,
	alpha=opacity,
	edgecolor='0.3',
	color='0.3',
	label='tmpfs_runsc_kvm')
	
	rects4 = plt.bar(index + 3*bar_width, averages['vol_tmpfs_kvm'], bar_width,
	alpha=opacity,
	edgecolor='0.1',
	color='0.1',
	label='vol_runsc_kvm')
	'''
	{'tmpfs_runsc_kvm': [0.5731536720273107, 2.205303125160041, 5.226133719942189, 6.335175024599456, 6.584671636579272], 'vol_tmpfs_kvm': [0.3633195247550703, 1.281117558881536, 2.664157137097065, 4.42655981338349, 5.7015168724377], 'tmpfs_bare': [4.278798307852268, 6.004261845873757, 6.253600685742584, 6.25475656014515, 5.96935709288597], 'tmpfs_runc': [3.671560781294868, 7.529840612659526, 6.307553666157148, 6.494765858027123, 6.866934252438734], 'runc': [4.000759089339324, 8.416811261257832, 6.727511369261703, 7.010305721693843, 7.301872877253718], 'runsc_ptrace': [0.26063085763994936, 0.9434745188110508, 2.1148263775561325, 3.706911087786844, 5.638134517587373], 'tmpfs_runsc_ptrace': [0.3141949481298467, 1.1377855099784728, 2.393350973579467, 4.159982742622373, 5.790682592250113], 'runsc_kvm': [0.3248270842573875, 1.1989001098381, 2.6603446773106576, 4.635091164634342, 6.428519245556698], 'bare': [4.751439508688163, 9.423307716514557, 7.523275748505955, 7.142106386200012, 7.34922766952992]}
	'''
	# Add text boxes (userspace_exit)
	ax.text(0.43,0.85,'47K') #tmpfs 4k	
	ax.text(1.43,2.35,'41K') #tmpfs 16K	
	ax.text(2.43,5.35,'28K') #tmpfs 64K	
	ax.text(3.43,6.5,'11K') #tmpfs 256K	
	ax.text(4.43,6.75,'0.7K') #tmpfs 1M	

	ax.text(0.63,0.5,'100K') #vol 4K	
	ax.text(1.63,1.5,'100K') #vol 16K	
	ax.text(2.63,2.75,'100K') #vol 64K	
	ax.text(3.63,4.55,'100K') #vol 256K	
	ax.text(4.63,6.0,'100K') #vol 1MB	

	plt.xlabel('Size of Read')
	plt.ylabel('Average Throughput (GB/s)')
	#plt.title('Throughput of Read')
	plt.xticks(index + 2*bar_width, ("4KB", "16KB", "64KB", "256KB", "1MB"))
	plt.xlim(left=-1*bar_width)
	plt.legend(loc = 'upper left')
	plt.ylim(top=13)	 
	plt.tight_layout()
	plt.savefig('./read_throughput.eps', format='eps', dpi=1000)
plt.show()
