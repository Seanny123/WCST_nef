import nengo
from nengo.utils.functions import piecewise
import matplotlib.pyplot as plt

#import ipdb

model = nengo.Network()

with model:
	input_1 = nengo.Node(1)
	input_2 = nengo.Node(-1)
	gate_1 = nengo.Node(0.5)
	gate_2 = nengo.Node(piecewise({0:1, 0.2:0, 0.4:0.5}))

	bg = nengo.networks.BasalGanglia(dimensions=2)
	thal = nengo.networks.Thalamus(dimensions=2, threshold=-1)

	nengo.Connection(gate_1, bg.input[0])
	nengo.Connection(gate_2, bg.input[1])
	nengo.Connection(bg.output, thal.input)
	nengo.Connection(input_1, thal.input[0])
	nengo.Connection(input_2, thal.input[1])

	bg_probe = nengo.Probe(bg.output, synapse=0.01)
	thal_probe = nengo.Probe(thal.output, synapse=0.01)

sim = nengo.Simulator(model)
sim.run(0.6)

fig = plt.figure()
plt.plot(sim.trange(), sim.data[bg_probe])

fig = plt.figure()
plt.plot(sim.trange(), sim.data[thal_probe])

plt.show()

#ipdb.set_trace()