import numpy as np
import nengo

# basically forward the signal that matters
class FakeBG(object):
	def __init__(self, dimensions, threshold):
		# the gate values, starting with the first
		self.state = np.zeros(dimensions)
		self.dimensions = dimensions
		self.state_index = 0
		self.state[self.state_index] = 1
		# the accumulated reward
		self.reward = 0
		self.threshold = threshold
		self.crossed = False

	def reward_input(self, t, x):
		"""mess with this later"""
		self.reward += x
		# if the reward passes the threshold, mark it
		# if the reward drops from the threshold, change the state
		if(self.reward > self.threshold):
			self.crossed = True
			print("CROSSED")
		elif(self.reward < self.threshold and self.crossed == True):
			self.crossed = False
			self.reward = 0
			# state stuff
			self.state = np.zeros(self.dimensions)
			self.state_index = (self.state_index + 1) % self.dimensions
			self.state[self.state_index] = 1
		elif(self.reward < 0):
			self.reward = 0

	def mem_gate(self, t):
		"""only train the memories while receiving reward"""
		if(self.reward > 0):
			return_val = np.ones(self.dimensions)
			return_val[self.state_index] = 0
			return return_val
		else:
			return np.ones(self.dimensions)

	def gate_output(self, t):
		return self.state

# dimensions should be renamed...
def make_bg(dimensions, threshold=1.0):
	with nengo.Network(label="fake basal_ganglia") as bg:
		fake_bg = FakeBG(dimensions, threshold)
		bg.reward_input = nengo.Node(fake_bg.reward_input, size_in=1)
		bg.gate_output = nengo.Node(fake_bg.gate_output, size_out=dimensions)
		bg.mem_gate = nengo.Node(fake_bg.mem_gate, size_out=dimensions)
	return bg

# I really feel like I need a mechanism to learn from failures, but I can't figure out how. I guess I have to run the model and find out the hard way.