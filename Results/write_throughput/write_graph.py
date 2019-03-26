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
	plt.rc('font', family='serif')
        plt.rc('xtick', labelsize='x-small')
        plt.rc('ytick', labelsize='x-small')
        fig = plt.figure(figsize=(3.5, 3))
        ax = fig.add_subplot(1, 1, 1)
	index = np.arange(n_groups)
	bar_width = 0.2
	opacity = 0.8
	plt.rcParams["figure.figsize"] = [3.5,2]	
	rects1 = plt.bar(index + 0*bar_width, averages['tmpfs_bare'], bar_width,
	edgecolor='0.8',
	color='0.8',
	alpha=opacity,
	label='bare')

	rects2 = plt.bar(index + 1*bar_width, averages['tmpfs_runc'], bar_width,
	edgecolor='0.3',
	color='0.3',
	alpha=opacity,
	label='runc')
	
	rect3 = plt.bar(index +  2*bar_width, averages['tmpfs_runsc_kvm'], bar_width,
	alpha=opacity,
	edgecolor='0.6',
	color='0.6',
	label='internal')
	
	rects4 = plt.bar(index + 3*bar_width, averages['vol_tmpfs_kvm'], bar_width,
	alpha=opacity,
	edgecolor='0.1',
	color='0.1',
	label='external')
	
	# Add text boxes (userspace_exit)
	'''
        ax.text(0.43,0.7,'47K',fontsize=10) #tmpfs 4k
        ax.text(1.43,2.15,'41K',fontsize=10) #tmpfs 16K
        ax.text(2.43,4.15,'28K',fontsize=10) #tmpfs 64K
        ax.text(3.43,5.4,'11K',fontsize=10) #tmpfs 256K
        ax.text(4.43,9.4,'0.7K',fontsize=10) #tmpfs 1M

        ax.text(0.63,0.4,'100K',fontsize=10) #vol 4K
        ax.text(1.63,1.43,'100K',fontsize=10) #vol 16K
        ax.text(2.63,2.33,'100K',fontsize=10) #vol 64K
        ax.text(3.63,3.43,'100K',fontsize=10) #vol 256K
        ax.text(4.63,4.0,'100K',fontsize=10) #vol 1MB
	'''

	plt.xlabel('Size of Write', fontsize=10)
	plt.ylabel('Throughput (GB/s)', fontsize=10)
	#plt.title('Throughput of Read')
	plt.xticks(index + 2*bar_width, ("4KB", "16KB", "64KB", "256KB", "1MB"))
	plt.xlim(left=-1*bar_width)
	plt.legend(loc = 'upper left', frameon=False, prop={'size':10}, ncol=2)
        ax.tick_params(axis=u'both', which=u'both',length=0)
	#plt.ylim(top=13)	 
	plt.tight_layout()
	plt.savefig('./write_throughput.eps', format='eps', dpi=1000)
plt.show()
