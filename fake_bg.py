import numpy as np

# basically forward the signal that matters
class FakeBG(object):
	def __init__(self, dimensions, threshold):
		# the gate values, starting with the first
		self.state = np.zeros(dimensions)
		self.state[0] = 1
		# the accumulated reward
		self.reward = 0

	def reward_input(self, t, x):
		"""mess with this later"""
		# if the reward passes the threshold, mark it
		# if the reward drops from the threshold, change the state


	def gate_output(self, t):
		return self.state

def make_bg(dimensions, threshold):
	with nengo.Network(label="fake basal_ganglia") as bg:
		bg = FakeBG(dimensions, threshold)
		bg.reward_input = nengo.Node(reward_input, size_in=1)
		bg.gate_output = nengo.Node(reward_input, size_out=dimensions)
	return bg


# Train the current transform if it's right
# Otherwise, discard it
# When the reward dies after multiple successes, switch rules

# I really feel like I need a mechanism to learn from failures, but I can't figure out how. I guess I have to run the model and find out the hard way.