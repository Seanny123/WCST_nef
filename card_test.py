import cards
import itertools
import nengo
import nengo.spa
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

wcst = cards.WCST(vocab)
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
# test category completion termination condition
# test deck exhaustion termination condition

#ipdb.set_trace()