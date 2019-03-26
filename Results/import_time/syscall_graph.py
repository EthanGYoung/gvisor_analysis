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
# results['numpy']= results['\ufeffnumpy']
# del results['\ufeffnumpy']
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
	bar_width = 0.1
	opacity = 0.8
	plt.rcParams["figure.figsize"] = [3.5,2]

	rects1 = plt.bar(index+1.5*bar_width, averages['mmap'], 3*bar_width,
	alpha=opacity,
	color='0.3')
	x = [0,1,2,3,4,5,6,7,8]
	plt1, = plt.plot(x, [65,65,65,65,65,65,65,65,65], color = 'gray', linewidth=2, linestyle='dashed')
	plt.legend( [plt1],["NO-OP"],loc ='upper right', frameon=False, prop={'size':10})

	plt.xlabel('Library Name',fontsize=10)
	plt.ylabel('Number of mmap()',fontsize=10)
	plt.xticks(index + 1.5*bar_width, ("django         ", "flask       ", "jinja2        ", "matplotlib             ","numpy         ","requests           ","setuptools              ", "sqlalchemy               ", "werkzeug             "),fontsize=8)
	ax.xaxis.get_majorticklabels()[0].set_y(+.13)
	ax.xaxis.get_majorticklabels()[1].set_y(+.12)
	ax.xaxis.get_majorticklabels()[2].set_y(+.12)
	ax.xaxis.get_majorticklabels()[3].set_y(+.17)
	ax.xaxis.get_majorticklabels()[4].set_y(+.13)
	ax.xaxis.get_majorticklabels()[5].set_y(+.15)
	ax.xaxis.get_majorticklabels()[6].set_y(+.18)
	ax.xaxis.get_majorticklabels()[7].set_y(+.19)
	ax.xaxis.get_majorticklabels()[8].set_y(+.18)
	plt.xticks(rotation=30)
	plt.xlim(left=-2*bar_width)

	plt.tight_layout()
	plt.savefig('./imports_mmap_result.eps', format='eps', dpi=1000)
plt.show()
