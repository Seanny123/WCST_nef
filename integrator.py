import nengo
from nengo.dists import Uniform

def ea_integrator(n_neurons, dimensions, input_scale=1.0, forget_rate=0.0, step_size=1.0):
	tau_PSC = 0.007
	int_PSC = 0.1

	input_weight = int_PSC * 1.0/step_size * input_scale
	# remember that the forget rate is super-approximate, but because of noisy values that's okay
	recur_weight = 1-(int_PSC * 1.0/step_size * forget_rate)

	with nengo.Network(label="ea_int") as ea_int:
		# TODO: specify ensemble parameters to be biologically plausible
		ea_int.input = nengo.Node(size_in=dimensions)
		ea_int.output = nengo.Node(size_in=dimensions)
		# WTF: Why more evaluation points?
		ea_int.integrator = nengo.networks.EnsembleArray(
			n_neurons, n_ensembles=dimensions, n_eval_points=dimensions*500,
			intercepts=Uniform(-1,1), max_rates=Uniform(100,200), 
			neuron_type=nengo.LIF(tau_rc=0.05, tau_ref=0.002)
		)
		nengo.Connection(ea_int.integrator.input, ea_int.integrator.output, transform=recur_weight, synapse=int_PSC)
		nengo.Connection(ea_int.input, ea_int.integrator.input, transform=input_weight, synapse=tau_PSC)
		# just to make this easier to connect to
		nengo.Connection(ea_int.integrator.output, ea_int.output, synapse=None)
	return ea_int