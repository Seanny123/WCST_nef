import nengo
import nengo.spa
from cards import card_net
from fake_bg import make_bg
from fake_gate import fake_gate
from eval_net import eval_net

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

# the cards is begin chosen at the BG right? should we inject noise into that thing then?

# Simulate until the card task is finished

wsct = WCST("pants")

model = nengo.Network(label="WCST")

# everything in direct mode at first
with model:
	cn = card_net(vocab)
	bg = make_bg(WCST_dimensions)
	en = eval_net(1, 1, WCST_dimensions, vocab)
	fg = fake_gate()
	ea_int = ea_integrator()

	# get the selected card into the card environment
	nengo.Connection(en.output, cn.input)
	# send the trial card to the evaluation network
	nengo.Connection(cn.trial_card, en.input)
	# send the feedback from the selection to the basal gangila
	nengo.Connection(cn.feedback, bg.reward_input)
	# hook up the basal ganglia to the gate and the memory selector
	nengo.Connection(bg.gate_output, fg.gate_in)
	# connect the memory outputs to the gate
	# connect the trial card result to the memories


sim = nengo.Simulator(model)
while(wcst.cat_num >= 6 and wcst.out_of_cards == False):
	sim.step()

# write out the results
output_file = open("results.txt", "w")
output_file.write("pers_err:%s" %(float(wcst.total_pers_error)/float(wcst.run_num)*100))
output_file.write("categories:%s" %wcst.cat_num)