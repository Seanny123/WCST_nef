import nengo
import ipdb
import fake_gate
import numpy as np
from nengo.utils.functions import piecewise

"""
gg = fake_gate.Gate(2, 3)
gg.set_input(1, np.array([1, 1, 1, 2, 2, 2]))
gg.set_gate(1, np.array([-1, 1]))

print(gg.output(1))
gg.set_gate(1, np.array([1, -1]))
print(gg.output(1))
"""

model = nengo.Network()

with model:
	input = nengo.Node(np.array([1,-1]))
	gate = nengo.Node(
		piecewise({
				0:np.array([0.5,1]),
				0.2:np.array([0.5,0]),
				0.4:np.array([0.5,0.5])
			})
	)
	#input_1 = nengo.Node(1)
	#input_2 = nengo.Node(-1)
	#gate_1 = nengo.Node(0.5)
	#gate_2 = nengo.Node(piecewise({0:1, 0.2:0, 0.4:0.5}))

	fg = fake_gate.fake_gate(inputs=2, input_dimensions=1)

	nengo.Connection(input, fg.input)
	nengo.Connection(gate, fg.gate_in)

	#nengo.Connection(input_1, fg.input[0])
	#nengo.Connection(input_2, fg.input[1])
	#nengo.Connection(gate_1, fg.gate_in[0])
	#nengo.Connection(gate_2, fg.gate_in[1])

	out_probe = nengo.Probe(fg.output, synapse=0.01)

sim = nengo.Simulator(model)
sim.run(0.6)

#fig = plt.figure()
#plt.plot(sim.trange(), sim.data[out_probe])

#plt.show()

#ipdb.set_trace()