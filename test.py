import nengo
import integrator
from nengo.utils.functions import piecewise

import ipdb

# Check if the integrator works

model = nengo.Network(label="test")
with model:
	input = nengo.Node(piecewise({0: [0,0], 0.2: [1,-1], 1: [0,0], 2: [-2,2], 3: [0,0], 4: [1,-1], 5: [0,0]}))
	# Dan technically only uses 25 neurons per dimension
	great = integrator.ea_integrator(100, 2, input_scale=0.4, forget_rate=0.2, step_size=0.2)
	#ipdb.set_trace()
	nengo.Connection(input, great.input, synapse=None)

	input_probe = nengo.Probe(input)
	output_probe = nengo.Probe(great.output, synapse=0.01)

sim = nengo.Simulator(model)
sim.run(6)
