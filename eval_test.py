import nengo
import numpy as np
import nengo.spa
import eval_net
from nengo.utils.functions import piecewise
import ipdb

# set up the vocab
vocab_d = 64
vocab = nengo.spa.Vocabulary(vocab_d, max_similarity=0.1, unitary=["ONE"], include_pairs=True)

# set up the inputs
colour_list = ["RED", "GREEN", "YELLOW", "BLUE"]
input_list = [vocab.parse("COLOUR*%s" %colour).v for colour in colour_list]
learn_dict = {0: np.zeros(vocab_d)}
for idx, i in enumerate(input_list):
	learn_dict[0.2*(1+idx)] = i

model = nengo.Network(label="test")
with model:
	input = nengo.Node(piecewise(learn_dict))
	e_n = eval_net.eval_net(50, 25, vocab_d, vocab)

	nengo.Connection(input, e_n.input)

	in_probe = nengo.Probe(input)
	#ipdb.set_trace()
	out_probe = nengo.Probe(e_n.output)

# simulate
sim = nengo.Simulator(model)
sim.run(0.2*(len(input_list)+1))

# plot the results
import matplotlib.pyplot as plt
fig = plt.figure()
plt.plot(sim.trange(), sim.data[in_probe])
fig = plt.figure()
plt.plot(sim.trange(), sim.data[out_probe])
plt.show()

ipdb.set_trace()