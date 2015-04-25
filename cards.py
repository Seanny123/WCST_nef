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

	def get_spa(self):
		return "%s*SHAPE+%s*COLOUR+%s*NUMBER" %(self.shape, self.colour, self.number)

class WCST(object):
	def __init__(self, vocab, output_file="results.txt"):

		# get SPA setup
		self.vocab = vocab

		# initialize card related things
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
		# Note that another option is to remove cards sharing  2+
		# attributes with stimulus cards
		# See Nelson HE: A modified card sorting test sensitive to 
		#        frontal lobe defects. Cortex 1976;12:313-324.

		# initialize settings
		self.rule_list = ["colour", "shape", "number"]
		self.last_rule = ""
		self.rule = ""
		self.run_num = 0
		self.run_length = 10
		self.output_file = output_file

		# initialize stat tracking
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

	def get_displayed(self, t):
		"""get the currently displayed cards
		not actually used since the similarity network 
		has them hard-coded at the moment

		Note: this should technically return a semantic pointer"""
		return self.displayed

	def get_trial(self, t):
		"""get the currently focused trial card"""
		return self.vocab.parse(self.trial.get_spa())

	def match(self, t, trial, selected):
		"""score the match"""
		feedback = False
		# if matched
		if(getattr(trial, self.rule) == getattr(selected, self.rule)):
			feedback = True
		else:
			# if it doesn't match any of the rules
			rule_match = False
			for rule in rule_list:
				if(getattr(trial, rule) == getattr(selected, rule)):
					rule_match = True
			if(rule_match == False):
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
			# if we return anything other than a boolean, things might explode
			return True

		# get a new trial card
		self.trial = self.deck.pop
		return feedback

	def write_result(self):
		print("result")
		self.output_file.write("Subnum trial run rule lastrule color shape number resp corr last_corr corr_col corr_shape corr_num persev persev_err abstime rt\n")

class FeedbackNode(object):
	# how much reward should I give and for how long?
	# I guess it doesn't matter since the basal ganglia set the threshold anyways
	# but it just feels kind of weird to give long continuous error
	# so we're going to time limit it
	# so that regardless of reaction time (which will be included later)
	# the same amount of reward will be given

	def __init__(self, feedback_timelimit =0.3, neg_reward=-0.1, pos_reward=0.1):
		self.timer = 0.0
		self.timelimit = timelimit
		self.neg_reward = neg_reward
		self.pos_reward = pos_reward



	def feedback_func(self, t, feedback):
		if(self.timer < self.timelimit)
			if(feedback):
				return self.pos_reward
			else:
				return self.neg_reward



def card_net():
	with nengo.Network(label="Card simulator") as card_sim:
