import itertools
import nengo
import nengo.spa
import numpy as np
import random

import ipdb

class Card(object):
	def __init__(self, number, shape, colour):
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
	"""note the test ends either two decks of 64 cards have been sorted or six categories have been achieved"""
	def __init__(self, vocab, card_step_size=0.5):

		# network specific stuff
		self.vocab = vocab
		self.card_step_size = card_step_size
		self.out_of_cards = False
		self.logfile = open("card_log.txt", "w")

		# initialize card related things
		colours = ["GREEN", "RED", "YELLOW", "BLUE"]
		numbers = ["ONE", "TWO", "THREE", "FOUR"]
		shapes = ["STAR", "CIRCLE", "TRIANGLE", "PLUS"]
		# create a deck full of cards
		self.disp = [
			("ONE","TRIANGLE","RED"),
			("TWO","STAR","GREEN"),
			("THREE","PLUS","YELLOW"),
			("FOUR","CIRCLE","BLUE")
		]
		self.displayed = []
		self.deck = []
		for card in itertools.product(numbers, shapes, colours):
			# get the displayed cards
			found = False
			for d in self.disp:
				if(card == d):
					self.displayed.append(card)
					found = True
					break
			if(found == False):
				self.deck.append(Card(*card))

		# just in case
		random.seed(0)
		#ipdb.set_trace()
		random.shuffle(self.deck)
		# in the official task, a deck of 128 cards is used
		# here we will use 64 cards and extrapolate from there
		# get the trial card
		self.trial = self.deck.pop()
		#initialize it with a silly value
		self.selected = self.trial
		# Note that another option is to remove cards sharing  2+
		# attributes with stimulus cards
		# See Nelson HE: A modified card sorting test sensitive to 
		#        frontal lobe defects. Cortex 1976;12:313-324.

		# initialize settings
		self.rule_list = ["colour", "shape", "number"]
		self.rule = self.rule_list[0]
		self.last_rule = ""
		self.run_num = 0
		# in the official task it's 10, but apparently 5 works pretty great
		# http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0063885
		self.run_length = 5

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
		self.first_cat = 0

		# just a flag for keeping track if a perservative error was made
		self.trial_pers_err = 0
		self.trial_persev = 0
		# this list of persevative responses, will be ignored for now
		self.persev = 0
		self.pers_run_list = []
		self.pers_run_flag = True

		self.feedback = 0.0

	def get_displayed(self, t):
		"""get the currently displayed cards
		not actually used since the similarity network 
		has them hard-coded at the moment

		Note: this should technically return a semantic pointer"""
		return self.displayed

	def get_trial(self, t):
		"""get the currently focused trial card"""
		return self.vocab.parse(self.trial.get_spa()).v

	def cc_res(self, t):
		return self.vocab.parse(  "%s*~(%s) + %s*~(%s)" %( self.trial.get_spa(),self.selected.get_spa(),self.trial.get_spa(),self.selected.get_spa() )  ).v

	def match(self, t, selected_vec):
		"""score the match, this is the method that synchronizes the whole network artificially

			there's a ton of different scores that you can get here, but the 
			perservative errors and categories are most important for me

			I adapted this from the PEBL scoring method in cardsort64.pbl
		"""
		if(t % self.card_step_size == 0.0 and not(self.out_of_cards)):
			self.selected = Card(*self.disp[np.argmax(np.array(selected_vec))])
			self.feedback = 0.0
			print(self.trial)
			print(self.selected)

			self.logfile.write("Trial:%s\n" %self.trial)
			self.logfile.write("Selected:%s\n" %self.selected)
			self.logfile.write("Rule:%s\n" %self.rule)

			# if matched
			if(getattr(self.trial, self.rule) == getattr(self.selected, self.rule)):
				print("MATCHED!")
				self.feedback = 1.0
				self.tot_corr += 1
				self.run_num += 1
			else:
				# if it doesn't match any of the rules
				rule_match = False
				for rule in self.rule_list:
					if(getattr(self.trial, rule) == getattr(self.selected, rule)):
						rule_match = True
				if(rule_match == False):
					self.unique_err += 1

			# if the last rule was matched
			if(self.last_rule != ""):
				if(getattr(self.trial, self.last_rule) == getattr(self.selected, self.last_rule)):
					# keep track of perservative responses
					self.tot_pers += 1
					self.persev += 1
					self.trial_pers_err = 0
					self.trial_persev = 1
				if(self.feedback == 0.0):
					# keep track of preservative errors
					self.tot_pers_err += 1
					self.trial_pers_err = 1

			if(self.run_num >= self.run_length):
				self.last_rule = self.rule
				self.cat_num += 1
				self.rule = self.rule_list[self.cat_num % 3]
				self.run_num = 0


				# I DO NOT UNDERSTAND THE PERSEVERATIVE FLAG THING
				# I will ignore it for now

				if(self.cat_num == 1):
					self.first_cat = self.trial_num

			if(len(self.deck) != 0):
				# get a new trial card
				self.trial = self.deck.pop()
			else:
				self.out_of_cards = True

			
			self.logfile.write("Feedback:%s\n" %self.feedback)

class FeedbackNode(object):
	# how much reward should I give and for how long?
	# I guess it doesn't matter since the basal ganglia set the threshold anyways
	# but it just feels kind of weird to give long continuous error
	# so we're going to time limit it
	# so that regardless of reaction time (which will be included later)
	# the same amount of reward will be given

	def __init__(self, timelimit=0.3, neg_reward=-0.1, pos_reward=0.1,  card_step_size=0.5):
		self.card_step_size = card_step_size
		self.timelimit = timelimit
		self.neg_reward = neg_reward
		self.pos_reward = pos_reward
		self.feedback = -1.0

	def set_feeback(self, t, x):
		self.feedback = float(x)

	def feedback_out(self, t):
		if(self.feedback == -1.0):
			return 0.0
		elif(t%self.card_step_size < self.timelimit):
			#print(self.feedback)
			if(self.feedback < 1.0):
				return self.neg_reward
			else:
				return self.pos_reward
		else:
				return 0.0

def card_net(vocab):
	with nengo.Network(label="Card simulator") as card_sim:
		feed = FeedbackNode()
		# only accessible for testing purposes
		card_sim.card_runner = WCST(vocab)

		card_sim.input = nengo.Node(card_sim.card_runner.match, size_in=4)
		card_sim.trial_card = nengo.Node(card_sim.card_runner.get_trial)
		card_sim.feedback = nengo.Node(feed.feedback_out, size_out=1)
		card_sim.cc_res = nengo.Node(card_sim.card_runner.cc_res, size_out=vocab.dimensions)

		# only accessible for debugging
		card_sim.feedback_input = nengo.Node(lambda t: card_sim.card_runner.feedback, size_out=1)

		nengo.Connection(card_sim.feedback_input, nengo.Node(feed.set_feeback, size_in=1), synapse=None)
	return card_sim