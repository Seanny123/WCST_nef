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