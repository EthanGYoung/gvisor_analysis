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
		mylist.append(mydict[key])
	return mylist

for platform in averages:
		averages[platform] = sort_keys(averages[platform])

if (sys.argv[2] == "bar"):
	n_groups = 10

	# create plot
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.1
	opacity = 0.8

	rects1 = plt.bar(index, averages['bare'], bar_width,
	alpha=opacity,
	color='0.1',
	label='bare')

	rects2 = plt.bar(index + 1*bar_width, averages['runc'], bar_width,
	alpha=opacity,
	color='0.3',
	label='runc')

	rects3 = plt.bar(index + 2*bar_width, averages['runc_tmpfs'], bar_width,
	alpha=opacity,
	color='0.5',
	label='runc_tmpfs')

	rects4 = plt.bar(index + 3*bar_width, averages['runsc_kvm'], bar_width,
	alpha=opacity,
	color='0.7',
	label='runsc_kvm')

	rects5 = plt.bar(index + 4*bar_width, averages['runsc_kvm_tmpfs'], bar_width,
	alpha=opacity,
	color='0.9',
	label='runsc_kvm_tmpfs')

	plt.xlabel('Library Name')
	plt.ylabel('Average Import Time (ms)')
	plt.xticks(index + 1.5*bar_width, ("django", "flask", "jinja2", "matplotlib","numpy","pip","requests","setuptools", "sqlalchemy", "werkzeug"))
	plt.xticks(rotation=30)
	plt.xlim(left=-2*bar_width)
	plt.legend(loc = 'upper left')

	plt.tight_layout()
	plt.savefig('./imports_result.eps', format='eps', dpi=1000)
plt.show()
