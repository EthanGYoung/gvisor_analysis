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
	if (data == 0):
		return 0
	return int(100000)/(data *1000000000) # GB/s

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
	plt.rc('font', family='serif')
	plt.rc('xtick', labelsize='x-small')
	plt.rc('ytick', labelsize='x-small')
	fig = plt.figure(figsize=(3.5, 2.5))
	ax = fig.add_subplot(1, 1, 1)
	n_groups = 5
	print(averages)
	# create plot
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

	plt.xlabel('Malloc Size', fontsize=10)
	plt.ylabel('Billions of Allocs/Second', fontsize=10)
	#plt.title('Throughput of Read')
	plt.xticks(index + 1.5*bar_width, ("1KB", "2KB", "4KB", "8KB", "16KB"))
	plt.xlim(left=-1*bar_width)
	plt.legend(loc = 'upper right', frameon=False, prop={'size':10})
	ax.tick_params(axis=u'both', which=u'both',length=0)
	# plt.ylim(top=13)
	plt.tight_layout()
	plt.savefig('./memory_nofree.eps', format='eps', dpi=1000)
plt.show()

