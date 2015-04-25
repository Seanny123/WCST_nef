import nengo
import ipdb
import fake_gate
import matplotlib.pyplot as plt
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
"""
gg = fake_gate.Gate(inputs=2, input_dimensions=1)
gg.set_input(1, np.array([1, 2]))
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
				0:np.array([-1,1]),
				0.2:np.array([0.5,0]),
				0.4:np.array([0.5,0.5]),
				0.6:np.array([1,-1]),
			})
	)

	fg = fake_gate.fake_gate(inputs=2, input_dimensions=1)

	nengo.Connection(input, fg.input)
	nengo.Connection(gate, fg.gate_in)

	out_probe = nengo.Probe(fg.output)

sim = nengo.Simulator(model)
sim.run(0.8)

fig = plt.figure()
plt.plot(sim.trange(), sim.data[out_probe], label="output")
plt.ylim(-1.25,1.25)
plt.show()
plt.legend()