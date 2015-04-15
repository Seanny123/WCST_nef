import nengo

class Swapper(object):
	def __init__(self, dimensions=128):
		self.last_val = np.zeros(dimensions)

	