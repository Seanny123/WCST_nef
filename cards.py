import itertools

class Card(object):
	def __init__(self, shape, colour, number):
		self.shape = shape
		self.colour = colour
		self.number = number

	def __str__(self):
		return "%s,%s,%s" %(self.shape, self.colour, self.number)

	def __repr__(self):
		return "Card:%s,%s,%s" %(self.shape, self.colour, self.number)

class WCST(object):
	def __init__(self):
		colours = ["GREEN", "RED", "YELLOW", "BLUE"]
		numbers = ["ONE", "TWO", "THREE", "FOUR"]
		shapes = ["STAR", "CIRCLE", "TRIANGLE", "PLUS"]
		# create a deck full of cards
		disp = [("ONE","TRIANGLE","RED"), ("TWO","STAR","GREEN"), ("THREE","PLUS","YELLOW"), ("FOUR","CIRCLE","BLUE")]
		self.displayed = []
		deck = []
		for card in itertools.product(numbers, shapes, colours):
			# get the displayed cards
			for d in disp:
				if(card == d):
					self.displayed.append(card)
					break
				else:
					deck.append(Card(*card))

		# get the trial card
		self.trial = deck.pop
		# initialize settings
		self.rule_list = ["colour", "shape", "number"]
		self.last_rule = ""
		self.rule = ""
		self.run_num = 0
		self.run_length = 10

		# Correct responses
		self.tot_corr = 0
		# Perseverative responses
		self.tot_pers = 0
		self.tot_pers_err = 0
		# Unique (no confusion) errors
		self.unique_err = 0
		# Number of trials
		self.trial_num = 0
		# Number of categories
		self.cat_num = 0
		# Trials to figure first category
		self.first_cat

		self.trial_pers_err = 0
		self.persev = 0

	def get_displayed(self):
		"""get the currently displayed cards, not actually used since the similarity network has them hard-coded at the moment"""
		return self.displayed

	def get_trial(self):
		"""get the currently focused trial card"""
		return self.trial

	def match(self, trial, selected):
		"""score the match"""
		feedback = False
		# if matched
		if(getattr(trial, self.rule) == getattr(selected, self.rule)):
			feedback = True
		else:
			# if it doesn't match any of the rules
			self.unique_err += 1

		# if the last rule was also matched
		if(self.last_rule != ""):
			if(getattr(trial, self.last_rule) == getattr(selected, self.last_rule)):
				self.tot_pers += 1
				self.persev += 1
			if(~feedback):
				self.tot_pers_err += 1
				self.trial_pers_err += 1


		if(self.run_num >= self.run_length):
			self.last_rule = self.rule
			#self.rule = #HOW TO GENERATE RULE?
			self.run_num = 0
			self.cat_num +=1

			# I DO NOT UNDERSTAND THE PERSEVERATIVE FLAG THING

			if(cat_num == 1):
				first_cat = self.trial_num

		if(cat_num >= 9):
			# why would this go over?
			self.cat_num = 9
			return "Done"

		# get a new trial card
		self.trial = self.deck.pop
		return feedback

	def write_result(self):
		print("result")
