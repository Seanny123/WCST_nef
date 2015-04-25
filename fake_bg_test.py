import nengo
import ipdb
import fake_bg
import matplotlib.pyplot as plt
import numpy as np
from nengo.utils.functions import piecewise

"""
fg = fake_bg.FakeBG(3, 1)
fg.reward_input(0, 3)
assert(fg.crossed == True)
assert(fg.state_index == 0)
fg.reward_input(0, -2.5)
assert(fg.crossed == False)
assert(fg.state_index == 1)

for _ in range(2):
	fg.reward_input(0, 3)
	fg.reward_input(0, -2.5)

assert(fg.state_index == 0)
ipdb.set_trace()
"""

model = nengo.Network()
dt = 0.01

with model:
	reward_input  = nengo.Node(piecewise({
			0:0,
			1.5:2*dt,
			2.5:-4*dt,
			3.5:0,
			4.5:2*dt,
			5.5:-4*dt,
			6.5:0
		}))

	fg = fake_bg.make_bg(3, 1)

	nengo.Connection(reward_input, fg.reward_input)

	gate_probe = nengo.Probe(fg.gate_output)
	# it seems to be working properly, but maybe also plot the accumulated reward?

sim = nengo.Simulator(model, dt=dt)
sim.run(6)

fig = plt.figure()
plt.plot(sim.trange(), sim.data[crossed_probe]*0.5, label="crossed")
plt.plot(sim.trange(), sim.data[reward_probe], label="reward")
plt.plot(sim.trange(), sim.data[gate_probe], label="gate")
plt.ylim(0,2)
plt.legend()
plt.show()