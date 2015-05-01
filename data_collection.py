# get data for the report

import nengo
import nengo.spa
import cards
from eval_net import eval_net
from transform_net import transform_net
import random
import ipdb
import numpy as np
from nengo.utils.functions import piecewise

WCST_dimensions = 128

vocab = nengo.spa.Vocabulary(WCST_dimensions, max_similarity=0.1, unitary=["ONE"], include_pairs=True)

tmp = vocab.parse("ONE")
vocab.add("TWO", vocab.parse("ONE*ONE"))
vocab.add("THREE", vocab.parse("ONE*TWO"))
vocab.add("FOUR", vocab.parse("ONE*THREE"))

tmp = cards.WCST(vocab)

red_trial = vocab.parse("NUMBER*ONE + SHAPE*CIRCLE + COLOUR*RED")
green_trial = vocab.parse("NUMBER*ONE + SHAPE*CIRCLE + COLOUR*GREEN")

yellow_1 = vocab.parse("NUMBER*ONE + SHAPE*TRIANGLE + COLOUR*YELLOW")
yellow_2 = vocab.parse("NUMBER*TWO + SHAPE*PLUS + COLOUR*YELLOW")

blue_1 = vocab.parse("NUMBER*TWO + SHAPE*PLUS + COLOUR*BLUE")
blue_2 = vocab.parse("NUMBER*THREE + SHAPE*STAR + COLOUR*BLUE")

green_1 = vocab.parse("NUMBER*FOUR + SHAPE*PLUS + COLOUR*GREEN")
green_2 = vocab.parse("NUMBER*ONE + SHAPE*STAR + COLOUR*GREEN")

yellow_feedback = yellow_2*~(yellow_1) + yellow_1*~(yellow_2)
blue_feedback = blue_2*~(blue_1) + blue_1*~(blue_2)
green_feedback = green_2*~(green_1) + green_1*~(green_2)


colours = ["GREEN", "RED", "YELLOW", "BLUE"]
numbers = ["ONE", "TWO", "THREE", "FOUR"]
shapes = ["STAR", "CIRCLE", "TRIANGLE", "PLUS"]

cleanup_pairs = []
for c in colours:
	cleanup_pairs.append(vocab.parse("COLOUR*%s" %(c)).v)
for n in numbers:
	cleanup_pairs.append(vocab.parse("NUMBER*%s" %(n)).v)
for s in shapes:
	cleanup_pairs.append(vocab.parse("NUMBER*%s" %(s)).v)

random.seed(0)
model = nengo.Network(label="WCST", seed=0)

p_neurons = 50
i_neurons = 50
m_neurons = 50
# This is the neurons per sub-ensemble because it uses an ensemble array
c_neurons = 200 # according to Xuan's and Jan's heuristic

with model:
	# show with the red card, if that works, switch to green
	trial_card = nengo.Node(piecewise({0:green_trial.v}), size_out=WCST_dimensions)
	#trans_input = nengo.Node(piecewise({0:yellow_feedback.v, 0.3:blue_feedback.v, 0.6:green_feedback.v}), size_out=WCST_dimensions)
	trans_input = nengo.Node(vocab.parse('0').v)

	en = eval_net(p_neurons, WCST_dimensions, vocab)
	t_net = transform_net(i_neurons, m_neurons, WCST_dimensions, input_scale=0.4, forget_rate=0.2, step_size=0.2, diff_gain=1.0)
	am = nengo.spa.AssociativeMemory(cleanup_pairs, default_output_vector=vocab.identity.v, n_neurons_per_ensemble=50)
	cconv = nengo.networks.CircularConvolution(c_neurons, WCST_dimensions)

	# send the trial card to circular convolution network
	nengo.Connection(trial_card, cconv.B, synapse=None)
	# trans_feedback into memory
	nengo.Connection(trans_input, t_net.mem_input.input, synapse=None)
	#nengo.Connection(trans_input, t_net.transform.input, synapse=None)
	#ipdb.set_trace()
	nengo.Connection(t_net.trans.output, am.input)
	nengo.Connection(am.output, cconv.A)
	nengo.Connection(cconv.output, en.input)

	p_am = nengo.Probe(am.output, synapse=0.05)
	p_sim = nengo.Probe(en.output, synapse=0.05)

ipdb.set_trace()

sim = nengo.Simulator(model)
sim.run(0.3)


import matplotlib.pyplot as plt

fig = plt.figure(); plt.plot(sim.trange(), sim.data[p_sim]); plt.legend(["red","green","yellow","blue"]); plt.show()

ipdb.set_trace()

# run with different differential gains

# run with different learning rates