import cards
import itertools
import ipdb

WCST_dimensions = 128

vocab = nengo.spa.Vocabulary(WCST_dimensions, max_similarity=0.1, unitary=["ONE"], include_pairs=True)

tmp = vocab.parse("ONE")
vocab.add("TWO", vocab.parse("ONE*ONE"))
vocab.add("THREE", vocab.parse("ONE*TWO"))
vocab.add("FOUR", vocab.parse("ONE*THREE"))

wcst = cards.WCST(vocab)
# get first wrong
wcst.trial_card("")
# get second right
# get n=8 more right
# did the rule switch?
# create a preservative error
# test category completion termination condition
# test deck exhaustion termination condition

model = nengo.Network(label="card simulator test")

with model:
	# same tests as before, but now check if the reward is running correctly
#ipdb.set_trace()