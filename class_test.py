import nengo
import ipdb
import numpy as np
from nengo.utils.functions import piecewise
 
class Tester(object):
 
	def __init__(self):
		self.shared_val = np.zeros(2)
 
	def set_shared(self, t, x):
		self.shared_val = np.array(x)
 
	def get_shared(self, t):
		return self.shared_val
 
with nengo.Network(label="class test") as net:
	tt = Tester()
	input = nengo.Node(
		piecewise(
			{
				0:np.array([1,-1]),
				0.5:np.array([2,-2]),
				1:np.array([-1,1])
			}
		)
	)
	net.input = nengo.Node(tt.set_shared, size_in=2)
	net.output = nengo.Node(tt.get_shared, size_out=2)
 
	nengo.Connection(input, net.input, synapse=0.005)
 
	p_in = nengo.Probe(input)
	p_out = nengo.Probe(net.output)
 
sim = nengo.Simulator(net)
sim.run(1)
 
import matplotlib.pyplot as plt
 
plt.plot(sim.trange(), sim.data[p_in])
plt.plot(sim.trange(), sim.data[p_out])
plt.show()