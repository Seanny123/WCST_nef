import nengo
import numpy as np

import sys
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose',
     color_scheme='Linux', call_pdb=1)

import ipdb

class Gate(object):
	def __init__(self, inputs, input_dimensions):

		self.input_dimensions = input_dimensions
		self.inputs = inputs
		self.gate_vals = np.zeros(inputs)
		self.input_vals =  np.zeros(inputs*input_dimensions)

	def set_input(self, t, x):
		self.input_vals = x

	def set_gate(self, t, x):
		self.gate_vals = x

	def output(self, t):
		# write anything with a gate value smaller than zero to zero
		# technically, the basal ganglia should make sure there
		# is only one value larger than the threshold
		out_dim = self.gate_vals[self.gate_vals>0].size
		if(out_dim == 0):
			return np.zeros(self.input_dimensions)
		elif(out_dim > self.input_dimensions):
			out_dim = self.input_dimensions
			return self.input_vals.reshape((self.inputs, self.input_dimensions))[np.where(self.gate_vals>0)[0][0]].reshape(out_dim*self.input_dimensions)
		else:
			#if(t > 0.8):
			#	ipdb.set_trace()
			return self.input_vals.reshape((self.inputs, self.input_dimensions))[self.gate_vals>0].reshape(out_dim*self.input_dimensions)


def fake_gate(inputs, input_dimensions):
	with nengo.Network(label="fake gate") as fg:
		gate = Gate(inputs, input_dimensions)
		fg.input = nengo.Node(
			gate.set_input,
			size_in=inputs*input_dimensions
		)
		fg.gate_in = nengo.Node(gate.set_gate, size_in=inputs)
		fg.output = nengo.Node(gate.output, size_out=input_dimensions)
	return fg