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
# results['bare']['NUMPY'].append(results['\ufeffbare']['NUMPY'][0])
# del results['\ufeffbare']
for platform in results:
	if (platform not in averages):
		averages[platform] = {}
	for size in results[platform]:
		averages[platform][size] = statistics.mean(results[platform][size])

# Sort keys inorder of size
def sort_keys(mydict):
	mylist = []

	keylist = sorted(mydict.keys())
	for key in keylist:
		print(key)
		mylist.append(mydict[key])
	return mylist

for platform in averages:
		averages[platform] = sort_keys(averages[platform])

print(averages)

if (sys.argv[2] == "bar"):
	n_groups = 9

	# create plot
	plt.rc('font', family='serif')
	plt.rc('xtick', labelsize='x-small')
	plt.rc('ytick', labelsize='x-small')
	fig = plt.figure(figsize=(3.5, 2.5))
	ax = fig.add_subplot(1, 1, 1)
	index = np.arange(n_groups)
	bar_width = 0.2
	opacity = 0.8
	plt.rcParams["figure.figsize"] = [3.5,2]

	rects1 = plt.bar(index, averages['bare'], bar_width,
	alpha=opacity,
	color='0.7',
	label='bare')

	rects2 = plt.bar(index + 1*bar_width, averages['runc_host_tmpfs'], bar_width,
	alpha=opacity,
	color='0.5',
	label='runc')

	rects3 = plt.bar(index + 2*bar_width, averages['runsc_sentry_tmpfs'], bar_width,
	alpha=opacity,
	color='0.3',
	label='internal')

	rects4 = plt.bar(index + 3*bar_width, averages['runsc_host_tmpfs'], bar_width,
	alpha=opacity,
	color='0.1',
	label='external')

	# rects5 = plt.bar(index + 4*bar_width, averages['runsc_kvm_tmpfs'], bar_width,
	# alpha=opacity,
	# color='0.9',
	# label='runsc_kvm_tmpfs')

	print("I'm here!")

	plt.xlabel('Library Name',fontsize=10)
	plt.ylabel('Average Import Time (ms)',fontsize=10)
	plt.xticks(index + 1.5*bar_width, ("django         ", "flask       ", "jinja2         ", "matplotlib          ","numpy         ","requests         ","setuptools         ", "sqlalchemy          ", "werkzeug         "))
	ax.xaxis.get_majorticklabels()[0].set_y(+.1)
	ax.xaxis.get_majorticklabels()[1].set_y(+.1)
	ax.xaxis.get_majorticklabels()[2].set_y(+.1)
	ax.xaxis.get_majorticklabels()[3].set_y(+.1)
	ax.xaxis.get_majorticklabels()[4].set_y(+.1)
	ax.xaxis.get_majorticklabels()[5].set_y(+.1)
	ax.xaxis.get_majorticklabels()[6].set_y(+.1)
	ax.xaxis.get_majorticklabels()[7].set_y(+.1)
	ax.xaxis.get_majorticklabels()[8].set_y(+.1)
	plt.xticks(rotation=30)
	plt.xlim(left=-2*bar_width)
	#plt.ylim(top=2000)
	plt.legend(loc = 'upper left', frameon=False, prop={'size':7})

	plt.tight_layout()
	plt.savefig('./imports_result.eps', format='eps', dpi=1000)
plt.show()
