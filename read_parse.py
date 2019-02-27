import numpy as np
import statistics
import sys
import matplotlib.pyplot as plt

def Average(lst):
	return sum(lst) / len(lst)

results = {}
found = False
cmd = ''
TYPE = ''
count = 0
with open(sys.argv[1], 'r') as file:
	for line in file:
		if found:
			time = line.split('average = ')[1]
			time = time.split(' seconds')[0]
			results[cmd].append(float(time))
			found = False
		if "platform" in line:
			TYPE = line.split('=')[1]
			print("New Type: " + str(TYPE))
		if "executing: " in line.lower():
			cmd = line.split(': ', 1)[1] + " " + str(TYPE)
			if (cmd not in results):
				results[cmd] = []
			found = True

for command in results:
	print("Command: " + str(command.strip('\n')))
	for val in results[command]:
		print(val)

	print('\n')

def convert_to_throughput(lst, size):
	for item in range(0, len(lst)):
		lst[item] = int(size) / (lst[item] * 1000000000) #GB/sec
	return lst



bare = {}
runc = {}
runsc_ptrace = {}
runsc_kvm = {}
mod_ptrace = {}
mod_kvm = {}
bare_std = {}
runc_std = {}
runsc_ptrace_std = {}
runsc_kvm_std = {}
mod_ptrace_std = {}
mod_kvm_std = {}

plot_results = {}
plot_results["bare"] = {}
plot_results["runc"] = {}
plot_results["runsc_ptrace"] = {}
plot_results["runsc_kvm"] = {}
plot_results["mod_ptrace"] = {}
plot_results["mod_kvm"] = {}

for command in results:
	print("Command: " + str(command.strip('\n')))
	size = int(command.split("100000 ")[1].split(" ./")[0])
	avg = Average(convert_to_throughput(results[command], size))
	std = statistics.stdev(results[command])
	if "runsc" in command:
		if "kvm" in command:
			if "mod" in command:
				mod_kvm[size] = avg	
				mod_kvm_std[size] = std	
				plot_results["mod_kvm"][size] = results[command]	

			else:
				runsc_kvm[size] = avg	
				runsc_kvm_std[size] = std	
				plot_results["runsc_kvm"][size] = results[command]	
		else:
			if "mod" in command:
				mod_ptrace[size] = avg	
				mod_ptrace_std[size] = std	
				plot_results["mod_ptrace"][size] = results[command]	

			else:
				runsc_ptrace[size] = avg	
				runsc_ptrace_std[size] = std	
				plot_results["runsc_ptrace"][size] = results[command]	
			
	elif "runc" in command:
		runc[size] = avg	
		runc_std[size] = std
		plot_results["runc"][size] = results[command]	

	else: #bare
		bare[size] = avg	
		bare_std[size] = std	
		plot_results["bare"][size] = results[command]	


for size in bare:
	print("Size: " + str(size))
	print("Bare: " + str(bare[size]))
	print("Runc: " + str(runc[size]))
	print("Runsc-ptrace: " + str(runsc_ptrace[size]))
	print("Runsc-kvm: " + str(runsc_kvm[size]))
	print("Mod-ptrace: " + str(mod_ptrace[size]))
	print("Mod-kvm: " + str(mod_kvm[size]))


def sort_keys(mydict):
	mylist = []
	
	keylist = mydict.keys()
	keylist.sort()
	for key in keylist:
		mylist.append(mydict[key])
	return mylist

final_bare = sort_keys(bare)
final_runc = sort_keys(runc)
final_runsc_ptrace = sort_keys(runsc_ptrace)
final_runsc_kvm = sort_keys(runsc_kvm)
final_mod_ptrace = sort_keys(mod_ptrace)
final_mod_kvm = sort_keys(mod_kvm)

print("Bare: " + str(bare))
print("Runc: " + str(runc))
print("Runsc-ptrace: " + str(runsc_ptrace))
print("Runsc-kvm: " + str(runsc_kvm))
print("Mod-ptrace: " + str(mod_ptrace))
print("Mod-kvm: " + str(mod_kvm))

bare_std = sort_keys(bare_std)
runc_std = sort_keys(runc_std)
runsc_ptrace_std = sort_keys(runsc_ptrace_std)
runsc_kvm_std = sort_keys(runsc_kvm_std)
mod_ptrace_std = sort_keys(mod_ptrace_std)
mod_kvm_std = sort_keys(mod_kvm_std)


n_groups = 5

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.1
opacity = 0.8
print(bare)

rects1 = plt.bar(index, final_bare, bar_width,
yerr = bare_std,
alpha=opacity,
color='0.3',
label='bare')

rects2 = plt.bar(index + 1*bar_width, final_runc, bar_width,
yerr = runc_std,
hatch='-',
alpha=opacity,
color='0.5',
label='runc')

rects3 = plt.bar(index +  2*bar_width, final_runsc_ptrace, bar_width,
yerr = runsc_ptrace_std,
alpha=opacity,
color='0.7',
label='runsc_ptrace')

rects4 = plt.bar(index + 3*bar_width, final_runsc_kvm, bar_width,
yerr = runsc_kvm_std,
alpha=opacity,
hatch='/',
color='0.9',
label='runsc_kvm')

rects5 = plt.bar(index + 4*bar_width, final_mod_ptrace, bar_width,
yerr = mod_kvm_std,
alpha=opacity,
color='r',
label='mod_ptrace')

rects6 = plt.bar(index + 5*bar_width, final_mod_kvm, bar_width,
yerr = runsc_kvm_std,
alpha=opacity,
color='b',
label='mod_kvm')

plt.xlabel('Write Size ')
plt.ylabel('Average Throughput (GB/Sec)')
plt.title('Throughput of Write System Call')
plt.xticks(index + 3*bar_width, ("4KB", "16KB", "64KB", "256KB", "1MB"))

plt.legend(loc = 'upper left')
 
plt.tight_layout()
plt.show()

