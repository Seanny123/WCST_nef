import nengo
import numpy as np

class OverrideNetwork(object):
	def __init__(self, dimensions):
		self.bg = 0.0
		self.bad = np.zeros(dimensions)
		self.normal = np.zeros(dimensions)
		self.dimensions = dimensions

	def override(self, t):
		return_val = np.zeros(dimensions)
		if(self.bg > 0.0):
			if(np.argmax(self.bad) == np.argmax(self.normal)):
		return_val[np.argmax(self.normal)] = 1
		return return_val




# take the similarity input and potentially over-ride it
def override_net(dimensions):
	with nengo.Network(label="override") as net:
		ovr = OverrideNetwork(dimensions)
		net.bg_input = nengo.Node(lambda t, x: ovr.bg = float(x), size_in=1)
		net.bad_t_res = nengo.Node(lambda t, x: ovr.bad = np.array(x), size_in=4)
		net.normal_res = nengo.Node(lambda t, x: over.normal = np.array(x), size_in=4)
		net.output = nengo.Node(override, size_out=4)
	return net