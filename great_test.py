import nengo
import integrator
from nengo.utils.functions import piecewise

import ipdb

# does the integrator stop holding it's value after you drop the input?

model = nengo.Network(label="test")
with model:
    input = nengo.Node(piecewise({0: [0,0], 0.2: [1,-1], 0.4: [0.5,-0.5], 0.6: [2,-2], 0.8: [1,-1], 1.0:[1,-1]}))

    #mem = nengo.networks.InputGatedMemory()
    # Dan technically only uses 25 neurons per dimension
    great = integrator.ea_integrator(100, 2, input_scale=0.4, forget_rate=0.2, step_size=0.2)
    #ipdb.set_trace()
    nengo.Connection(input, great.input, synapse=None)

    input_probe = nengo.Probe(input)
    output_probe = nengo.Probe(great.output, synapse=0.01)

    actual = nengo.Node(piecewise({0: [0,0], 0.2:[0.5,-0.5], 0.4:[0.5, -0.5], 0.6:[0.875,-0.875], 0.8:[0.9,-0.9]}))
    actual_probe = nengo.Probe(actual)

sim = nengo.Simulator(model)
sim.run(2)

import matplotlib.pyplot as plt

plt.plot(sim.trange(), sim.data[output_probe])
plt.plot(sim.trange(), sim.data[actual_probe])
plt.show()

ipdb.set_trace()

# 