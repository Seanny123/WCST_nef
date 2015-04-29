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
		self.reward_acc = 0
		self.received_reward = 0
		self.threshold = threshold
		self.crossed = False
		self.reward_factor = 3.0
		self.max_reward = 1.0 + 2*self.reward_factor

	def reward_input(self, t, x):
		"""mess with this later"""
		# I've arbitrarily chosen a streak of 3 to be ideal, with no actual evidence for this
		self.received_reward = float(x)
		self.reward_acc += float(x)/self.reward_factor
		# if the reward passes the threshold, mark it
		# if the reward drops from the threshold, change the state
		if(self.reward_acc > self.threshold):
			self.crossed = True
			#print("CROSSED")
		elif(self.reward_acc < self.threshold and self.crossed == True):
			self.crossed = False
			self.reward_acc = 0
			# state stuff
			self.state = np.zeros(self.dimensions)
			self.state_index = (self.state_index + 1) % self.dimensions
			self.state[self.state_index] = 1
		elif(self.reward_acc < 0):
			self.reward_acc = 0
		elif(self.reward_acc > self.max_reward):
			self.reward_acc = self.max_reward


	def mem_gate(self, t):
		"""only train the memories while receiving reward"""
		if(self.received_reward > 0):
			return_val = np.ones(self.dimensions)
			return_val[self.state_index] = 0
			return return_val
		else:
			return np.ones(self.dimensions)

	def override_gate(self, t):
		"""override the similarity if we've crossed, or we've just started"""
		if(self.crossed or self.reward_acc == 0):
			return 1.0
		else:
			return 0.0

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