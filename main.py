import nengo
import nengo.spa

WCST_dimensions = 128

vocab = nengo.spa.Vocabulary(WCST_dimensions)

# prove that neurally this stuff works
# first with rigged training case
# then see how long it takes for it to find that first rule
# the dangers of putting our faith in randomness

model = spa.SPA(label="Simple question answering")

with model:
	model.colour_in = spa.Buffer(dimensions=WCST_dimensions)
	model.shape_in = spa.Buffer(dimensions=WCST_dimensions)
	model.number_in = spa.Buffer(dimensions=WCST_dimensions)

	# I think I want this to be a memory...
	model.transform = spa.

	# connect the buffers... Somehow...
	cortical_actions = spa.Actions(

	)

# So, hypothetically, I could do the flow control (trial, compute transform, another trial, compute another transform) with the basal ganglia, but I can also just do it with code, right?