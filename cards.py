# combinatorics library

class Card(object):
	def __init__(self, shape, colour, number):
		self.shape = shape
		self.colour = colour
		self.number = number

class WCST(object):
	def __init__(self):
		colours = ""
		# create a deck full of cards
		# create the displayed cards
		# get the trial card
		# initialize settings
		self.rule_list = ["colour", "shape", "number"]
		self.last_rule = ""
		self.rule = ""
		self.run_length = 10

	def get_displayed(self):
		"""get the currently displayed cards"""
		return self.displayed

	def get_trial(self):
		"""get the currently focused trial card"""
		return self.trial

	def match(self, trial, selected):
		# score the match
		feedback = False
		if(getattr(trial, self.rule) == getattr(selected, self.rule)):
			feedback = True
		if(self.last_rule != ""):
			if(getattr(trial, self.last_rule) == getattr(selected, self.last_rule)):


		# get a new trial card
		self.trial = self.deck.pop
		return feedback

