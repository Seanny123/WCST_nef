import cards
import itertools
import nengo
import nengo.spa
from nengo.utils.functions import piecewise
import ipdb

#import sys
#from IPython.core import ultratb
#sys.excepthook = ultratb.FormattedTB(mode='Verbose',
#     color_scheme='Linux', call_pdb=1)

WCST_dimensions = 128

vocab = nengo.spa.Vocabulary(WCST_dimensions, max_similarity=0.1, unitary=["ONE"], include_pairs=True)

tmp = vocab.parse("ONE")
vocab.add("TWO", vocab.parse("ONE*ONE"))
vocab.add("THREE", vocab.parse("ONE*TWO"))
vocab.add("FOUR", vocab.parse("ONE*THREE"))

"""
# these unit test should really be decoupled... oops
wcst = cards.WCST(vocab)
wcst.run_length = 10
# get first wrong
wcst.trial = cards.Card("TWO", "TRIANGLE","BLUE")
wcst.match(0.5, [1,0,0,0])
assert(wcst.feedback == False)
# get second right
wcst.trial = cards.Card("TWO", "TRIANGLE","BLUE")
wcst.match(0.5, [0,0,0,1])
assert(wcst.feedback == True)
# get n=9 more right
for i in range(9):
	wcst.trial = cards.Card("TWO", "TRIANGLE","BLUE")
	wcst.match(0.5, [0,0,0,1])
# did the rule switch?
assert(wcst.rule == "shape")
# do all rules work?
for i in range(10):
	wcst.trial = cards.Card("TWO", "TRIANGLE","BLUE")
	wcst.match(0.5, [1,0,0,0])
assert(wcst.rule == "number")
wcst.trial = cards.Card("TWO", "TRIANGLE","BLUE")
wcst.match(0.5, [0,1,0,0])
assert(wcst.feedback == True)

# create a preservative error
for i in range(10):
	wcst.trial = cards.Card("TWO", "TRIANGLE","BLUE")
	wcst.match(0.5, [0,1,0,0])
assert(wcst.tot_pers_err == 1)
assert(wcst.cat_num == 3)

# test category completion termination condition
wcst = cards.WCST(vocab)
for i in range(9):
	wcst.trial = cards.Card("TWO", "TRIANGLE","BLUE")
	wcst.match(0.5, [1,0,0,0])

# test deck exhaustion termination condition
wcst = cards.WCST(vocab)
wcst.deck = []
wcst.match(0.5, [1,0,0,0])
assert(wcst.out_of_cards == True)
"""

# test reward timing with a network
# also tests node functionality
model = nengo.Network(label="reward test")

with model:
	selected_input = nengo.Node(piecewise({0:[0,0,0,1], 0.6:[0,0,1,0]}))

	cn = cards.card_net(vocab)
	cn.card_runner.deck = [cards.Card("TWO", "TRIANGLE","BLUE")] * 5
	cn.card_runner.trial = cards.Card("TWO", "TRIANGLE","BLUE")

	nengo.Connection(selected_input, cn.input)

	reward_probe = nengo.Probe(cn.feedback)
	feed_probe = nengo.Probe(cn.feedback_input)

# WHY THE FUCK WOULD CHANING DT CHANGE THE FUCKING RESULT
sim = nengo.Simulator(model, dt=0.01)
sim.run(2.0)

import matplotlib.pyplot as plt

fig = plt.figure()
plt.plot(sim.trange(), sim.data[reward_probe])
plt.plot(sim.trange(), sim.data[feed_probe]*0.5)
plt.show()