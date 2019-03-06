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
		averages[platform][size] = throughput(statistics.mean(results[platform][size]),size)

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
	rects1 = plt.bar(index + 0*bar_width, averages['bare'], bar_width,
	edgecolor='0.8',
	color='0.8',
	alpha=opacity,
	label='bare')

	rects2 = plt.bar(index + 1*bar_width, averages['runc'], bar_width,
	edgecolor='0.6',
	color='0.6',
	alpha=opacity,
	label='runc')

	rect3 = plt.bar(index +  2*bar_width, averages['runsc_kvm'], bar_width,
	alpha=opacity,
	edgecolor='0.3',
	color='0.3',
	label='gVisor')

	# rects4 = plt.bar(index + 3*bar_width, averages['vol_tmpfs_kvm'], bar_width,
	# alpha=opacity,
	# edgecolor='0.1',
	# color='0.1',
	# label='vol_runsc_kvm')
	'''
	{'tmpfs_runsc_kvm': [0.556838039781646, 2.0169383129511527, 4.0217951793116855, 5.240230747895047, 9.258899609481917], 'vol_tmpfs_kvm': [0.34603979082661745, 1.2131831773217212, 2.157168939936002, 3.2391736955930015, 3.888379175683941], 'tmpfs_bare': [3.9052208989726984, 3.6617424142918162, 3.613216550038702, 3.8302585729444862, 3.9853288961084226], 'tmpfs_runc': [3.1281758841940737, 5.8708276520755325, 3.6200574253041307, 4.053075424678818, 4.1322747320988675], 'runc': [2.259245784110025, 3.752393384670628, 2.835614644433353, 3.2213169924505136, 2.9210823332013525], 'runsc_ptrace': [0.23189166363424635, 0.7694154871798214, 1.3157206119639493, 2.153795273223762, 2.159107833902489], 'tmpfs_runsc_ptrace': [0.30288969667099497, 1.07729114053848, 2.1876560175970674, 3.926678460729467, 7.97516740402894], 'runsc_kvm': [0.30295204938274617, 0.9982702646248316, 1.7627591928250985, 2.550841304436869, 2.4256062977308464], 'bare': [2.755770801708155, 3.998135049603084, 2.9846346376331523, 1.724422103978146, 1.3317308198884121]}
	'''

	# Add text boxes (userspace_exit)
	# ax.text(0.43,0.7,'47K') #tmpfs 4k
	# ax.text(1.43,2.15,'41K') #tmpfs 16K
	# ax.text(2.43,4.15,'28K') #tmpfs 64K
	# ax.text(3.43,5.4,'11K') #tmpfs 256K
	# ax.text(4.43,9.4,'0.7K') #tmpfs 1M
	#
	# ax.text(0.63,0.4,'100K') #vol 4K
	# ax.text(1.63,1.43,'100K') #vol 16K
	# ax.text(2.63,2.33,'100K') #vol 64K
	# ax.text(3.63,3.43,'100K') #vol 256K
	# ax.text(4.63,4.0,'100K') #vol 1MB

	plt.xlabel('Malloc Size')
	plt.ylabel('Average Throughput (GB/s)')
	#plt.title('Throughput of Read')
	plt.xticks(index + 2*bar_width, ("4KB", "16KB", "64KB", "256KB", "1MB"))
	plt.xlim(left=-1*bar_width)
	plt.legend(loc = 'upper left')
	# plt.ylim(top=13)
	plt.tight_layout()
	plt.savefig('./memory_nofree.eps', format='eps', dpi=1000)
plt.show()
