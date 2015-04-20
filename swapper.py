import nengo
import numpy as np

from nengo.utils.functions import piecewise

class Swapper(object):
	def __init__(self, vocab, dimensions=128):
		self.dimensions = dimensions
		self.vocab = vocab
		self.last_val = vocab.parse('0').v

		# test repeating attributes later
		green_row_1 = vocab.parse("NUMBER*ONE + SHAPE*TRIANGLE + COLOUR*GREEN")
		green_row_2 = vocab.parse("NUMBER*TWO + SHAPE*PLUS + COLOUR*GREEN")
		green_row_3 = vocab.parse("NUMBER*THREE + SHAPE*STAR + COLOUR*GREEN")
		# test swapping rules later
		yellow_row_1 = vocab.parse("NUMBER*ONE + SHAPE*TRIANGLE + COLOUR*YELLOW")
		yellow_row_2 = vocab.parse("NUMBER*TWO + SHAPE*PLUS + COLOUR*YELLOW")
		yellow_row_3 = vocab.parse("NUMBER*THREE + SHAPE*STAR + COLOUR*YELLOW")

		self.input_list = [green_row_2*~(green_row_1)]#, green_row_3*~(green_row_2), yellow_row_2*~(yellow_row_1)]
		learn_dict = {0: np.zeros(dimensions)}
		for idx, i in enumerate(self.input_list):
			learn_dict[0.2*(1+idx)] = i.v/(idx+1)
		self.default_output = piecewise(learn_dict)

		self.trange = 0.2*(len(self.input_list)+1)

	def save_stuff(self, t, x):
		if(t < self.trange):
			# apparently this fucks everything up, which is weird
			#print("setting last_val")
			self.last_val = x

	def output(self, t):
		if(t < self.trange):
			#return self.vocab.parse('0').v
			return self.default_output(t)
		elif(t >= self.trange and t < self.trange + 0.4):
			# this is apparently not how you create zero
			return self.vocab.parse('0').v
		else:
			#print("last_val")
			return self.last_val