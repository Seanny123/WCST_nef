import nengo
import numpy as np


class OverrideNetwork(object):
	def __init__(self, dimensions):
		self.bg = 0.0
		self.bad = np.zeros(dimensions)
		self.normal = np.zeros(dimensions)

	def override(self, t, x):


# take the similarity input and potentially over-ride it
def override_net(dimensions):
	with nengo.Network(label="override") as net:
		ovr = OverrideNetwork(dimensions)
		net.bg_input = nengo.Node(lambda t, x: ovr.bg_val = x)
		net.bad_t_res = nengo.Node(lambda t, x: ovr.bad = x)
		net.normal_res = nengo.Node(lambda t, x: over.normal = x)
		net.output = nengo.Node(override, size_out=4)
	return net