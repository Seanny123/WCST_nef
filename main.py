import nengo
import nengo.spa

WCST_dimensions = 128

vocab = nengo.spa.Vocabulary(WCST_dimensions)

# prove that neurally this stuff works
# first with rigged training case
# then see how long it takes for it to find that first rule
# the dangers of putting our faith in randomness

# Simulate until the card task is finished

wsct = WCST("pants")

model = nengo.Network(label="WCST")

with model:

sim = nengo.Simulator(model)
while(wcst.cat_num >= 6 and wcst.out_of_cards == False):
	sim.step()

# write out the results