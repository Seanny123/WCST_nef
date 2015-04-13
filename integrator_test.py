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

    input = nengo.Node(piecewise(learn_dict))
    trial = nengo.Node(piecewise(trial_dict))
    green_node = nengo.Node(vocab.parse("NUMBER*ONE + SHAPE*TRIANGLE + COLOUR*GREEN").v)
    blue_node = nengo.Node(vocab.parse("NUMBER*TWO + SHAPE*CIRCLE + COLOUR*BLUE").v)

    # Dan technically only uses 25 neurons per dimension and only 25 dimensions
    great = integrator.ea_integrator(100, vocab_d, input_scale=0.4, forget_rate=0.2, step_size=0.2)
    cconv = nengo.networks.CircularConvolution(100, 128)
    
    
    res_green = nengo.Ensemble(100)
    res_blue = nengo.Ensemble(100)
    nengo.Connection(input, great.input, synapse=None)
    nengo.Connection(great.output, cconv.A)
    nengo.Connection(trial, cconv.B)

    input_probe = nengo.Probe(input)
    output_probe = nengo.Probe(cconv.output, synapse=0.01)
    green_probe = nengo.Probe(res_green, synapse=0.01)
    blue_probe = nengo.Probe(res_red, synpase=0.01)