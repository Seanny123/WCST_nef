# read in each line
fi = open("forget_results.txt", "r").read().split("\n")
forget_list = [0.15, 0.2, 0.25]
sample_times = {0.29:[], 0.59:[], 0.89:[]}
forget_data = {}
for f in forget_list:
	forget_data[f] = sample_times

for line in fi:
	splitted = line.split(";")
	tmp = eval(splitted[2])
	for k, v in tmp.iteritems():
		forget_data[splitted[1]][k].append(v)
# create an average for each time step
# make some graphs

fig = plt.figure()
plt.title("Forget rate effect")
for f in forget_list:
	plt.ylabel("Distance from correct value")
	plt.xlabel("Time (s)")
	plt.plot(forget_data[f].keys(), np.mean(forget_data[f].values()) yerr=ss.t.ppf(0.95, len(forget_data[f].values))*np.std(forget_data[f].values()), label="rate=%s" %f)
plt.legend()
plt.savefig("forget_plot")