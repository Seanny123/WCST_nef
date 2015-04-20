import ipdb

import nengo.spa
import nengo
from nengo.utils.functions import piecewise

# set up the vocab
# similarity taken from RPM
# dimensions found by trial and error
vocab_d = 128
vocab = nengo.spa.Vocabulary(vocab_d, max_similarity=0.1, unitary=["ONE"], include_pairs=True)

tmp = vocab.parse("ONE")
vocab.add("TWO", vocab.parse("ONE*ONE"))
vocab.add("THREE", vocab.parse("ONE*TWO"))
vocab.add("FOUR", vocab.parse("ONE*THREE"))

# test repeating attributes later
green_row_1 = vocab.parse("NUMBER*ONE + SHAPE*TRIANGLE + COLOUR*GREEN")
green_row_2 = vocab.parse("NUMBER*TWO + SHAPE*PLUS + COLOUR*GREEN")
green_row_3 = vocab.parse("NUMBER*THREE + SHAPE*STAR + COLOUR*GREEN")
# test swapping rules later
yellow_row_1 = vocab.parse("NUMBER*ONE + SHAPE*TRIANGLE + COLOUR*YELLOW")
yellow_row_2 = vocab.parse("NUMBER*TWO + SHAPE*PLUS + COLOUR*YELLOW")
yellow_row_3 = vocab.parse("NUMBER*THREE + SHAPE*STAR + COLOUR*YELLOW")

trial_card = vocab.parse("NUMBER*ONE + SHAPE*CIRCLE + COLOUR*GREEN")

import numpy as np

# make the inputs
input_list = [green_row_2*~(green_row_1)]#, green_row_3*~(green_row_2), yellow_row_2*~(yellow_row_1)]
learn_dict = {0: np.zeros(vocab_d)}
for idx, i in enumerate(input_list):
    learn_dict[0.2*(1+idx)] = i.v/(idx+1)

trial_dict = {0.0:trial_card.v}

import eval_net
import integrator
import swapper

# testing swapping memories
sw = swapper.Swapper(vocab, vocab_d)

model = nengo.spa.SPA(label="transform test", seed=0)

# direct neurons to start
direct = True
if(direct ==  True):
    # Because setting them all to 1 has weird effects
    model.config[nengo.Ensemble].neuron_type = nengo.Direct()
    p_neurons = 5
    e_neurons = 5
    i_neurons = 5
    c_neurons = 10
else:
    p_neurons = 50
    e_neurons = 25
    i_neurons = 50
    c_neurons = 50*vocab_d # according to Xuan's heuristic

with model:
    input = nengo.Node(sw.output, size_in=0, size_out=vocab_d)
    mem = nengo.Node(sw.save_stuff, size_in=vocab_d, size_out=0)
    trial = nengo.Node(piecewise(trial_dict))
    e_n = eval_net.eval_net(p_neurons, e_neurons, vocab_d, vocab)

    # Dan technically only uses 25 neurons per dimension and only 25 dimensions
    great = integrator.ea_integrator(i_neurons, vocab_d, input_scale=0.4, forget_rate=0.2, step_size=0.2)
    # is this a really silly amount of neurons? # okay, can I just make this direct?
    cconv = nengo.networks.CircularConvolution(c_neurons, 128)
        
    nengo.Connection(input, great.input, synapse=None)
    nengo.Connection(great.output, cconv.A)
    nengo.Connection(great.output, mem, synapse=None)
    nengo.Connection(trial, cconv.B)
    nengo.Connection(cconv.output, e_n.input)
    

    input_probe = nengo.Probe(input)
    cc_probe = nengo.Probe(cconv.output, synapse=0.01)
    output_probe = nengo.Probe(e_n.output, synapse=0.01)

sim = nengo.Simulator(model)
sim.run(0.2*(len(input_list)+1)*2 + 0.4)

import matplotlib.pyplot as plt

fig = plt.figure()
plt.plot(sim.trange(), sim.data[output_probe])
plt.legend(["red","green","yellow","blue"])
fig = plt.figure()
plt.plot(sim.trange(), sim.data[input_probe])
plt.show()

ipdb.set_trace()

# if this doesn't work, try it with the most basic node-network