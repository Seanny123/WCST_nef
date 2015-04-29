import nengo
import nengo.spa
from cards import card_net
import cards
from fake_bg import make_bg
from fake_gate import fake_gate
from eval_net import eval_net
from transform_net import super_t
import random
import ipdb

WCST_dimensions = 128

vocab = nengo.spa.Vocabulary(WCST_dimensions, max_similarity=0.1, unitary=["ONE"], include_pairs=True)

tmp = vocab.parse("ONE")
vocab.add("TWO", vocab.parse("ONE*ONE"))
vocab.add("THREE", vocab.parse("ONE*TWO"))
vocab.add("FOUR", vocab.parse("ONE*THREE"))

# prove that neurally this stuff works
# first with rigged training case
# then see how long it takes for it to find that first rule
# the dangers of putting our faith in randomness

# Simulate until the card task is finished
random.seed(0)
model = nengo.Network(label="WCST", seed=0)

# everything in direct mode at first
direct = True
repeats = True
if(direct ==  True):
    # Because setting them all to 1 has weird effects
    model.config[nengo.Ensemble].neuron_type = nengo.Direct()
    p_neurons = 5
    e_neurons = 5
    i_neurons = 5
    m_neurons = 5
    c_neurons = 10
else:
    p_neurons = 50
    e_neurons = 25
    i_neurons = 50
    m_neurons = 50
    # This is the neurons per sub-ensemble because it uses an ensemble array
    c_neurons = 200 # according to Xuan's and Jan's heuristic

with model:
	cn = card_net(vocab)
	# rig the deck for testing
	#cn.card_runner.deck = [cards.Card("TWO", "TRIANGLE","BLUE")] * 1
	#cn.card_runner.trial = cards.Card("TWO", "TRIANGLE","BLUE")
	cn.card_runner.deck = cn.card_runner.deck[0:3]

	bg = make_bg(4)
	en = eval_net(p_neurons, e_neurons, WCST_dimensions, vocab)
	fg = fake_gate(4, WCST_dimensions)
	st = super_t(i_neurons, m_neurons, WCST_dimensions, input_scale=0.4, forget_rate=0.2, step_size=0.2, diff_gain=1.0)
	cconv = nengo.networks.CircularConvolution(c_neurons, WCST_dimensions)

	# get the selected card into the card environment
	nengo.Connection(en.output, cn.input, synapse=None)
	# send the trial card to circular convolution network
	nengo.Connection(cn.trial_card, cconv.B, synapse=None)
	# send the feedback from the selection to the basal gangila
	nengo.Connection(cn.feedback, bg.reward_input, synapse=None)
	# hook up the basal ganglia to the gate and the memory selector
	nengo.Connection(bg.gate_output, fg.gate_in, synapse=None)
	# connect the memory outputs to the gate
	nengo.Connection(bg.mem_gate, st.gate, synapse=None)
	# connect the trial card result to the memories
	nengo.Connection(cn.cc_res, st.input, synapse=None)
	# connect memory output to the gate
	nengo.Connection(st.output, fg.input)
	if(not(direct)):
		nengo.Connection(fg.output, cconv.A)
	else:
		bonus = nengo.Node
	nengo.Connection(cconv.output, en.input)

	#if(not(repeats)):
	#	nr = no_repeats_net()
	#	ovr = override_net()

	# probe the reward, gate, trial and similarity values
	p_in_r = nengo.Probe(cn.feedback_input)
	p_reward = nengo.Probe(cn.feedback)
	p_bg = nengo.Probe(bg.mem_gate)
	p_gate = nengo.Probe(bg.gate_output)
	p_sim = nengo.Probe(en.output)
	# is cconv working?
	p_cconv = nengo.Probe(cconv.output, synapse=0.01)
	# WHY YOU ZERO? BECAUSE TRANSFORM IS ZERO? OH GOD.
	p_A = nengo.Probe(fg.output)
	p_B = nengo.Probe(cn.trial_card)

	# a summary of the behaviour will be printed out by the simulation environment


sim = nengo.Simulator(model)
step_count = 0
print("Simulating")
while(cn.card_runner.out_of_cards == False):
	step_count += 1
	if(step_count % 1000 == 0):
		print("Step:%s" %step_count)
		print("Cards:%s" %len(cn.card_runner.deck))
	sim.step()

import matplotlib.pyplot as plt

plt.plot(sim.trange(), sim.data[p_in_r]*0.5)
plt.plot(sim.trange(), sim.data[p_reward])
plt.show()

ipdb.set_trace()

# write out the results # this is not working
output_file = open("results.txt", "w")
output_file.write("pers_err:%s" %(float(cn.card_runner.total_pers_err)/float(cn.card_runner.run_num)*100))
output_file.write("categories:%s" %cn.card_runner.cat_num)


plt.plot(sim.trange(), sim.data[p_A]); plt.show()

plt.plot(sim.trange(), sim.data[p_bg]); plt.show()