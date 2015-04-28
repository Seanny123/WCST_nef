import nengo
from integrator import ea_integrator

# how to efficiently pass parameters?
def transform_net(int_neurons, mem_neurons, dimensions, input_scale=1.0, forget_rate=0.0, step_size=1.0, diff_gain=1.0):
	with nengo.Network(label="transform") as t_n:
		t_n.mem_input = nengo.networks.workingmemory.InputGatedMemory(mem_neurons, dimensions, difference_gain=diff_gain)
		t_n.transform = ea_integrator(int_neurons, dimensions, input_scale, forget_rate, step_size)
		nengo.Connection(t_n.mem_input.output, t_n.transform.input)
	return t_n

def super_t(int_neurons, mem_neurons, dimensions, input_scale=1.0, forget_rate=0.0, step_size=1.0, diff_gain=1.0):
	"""just to make it easier to connect to"""
	with nengo.Network(label="transform container") as s_t:
		s_t.input = nengo.Node(size_in=dimensions)
		s_t.output = nengo.Node(size_in=dimensions*4)
		s_t.gate = nengo.Node(size_in=4)

		t1 = transform_net(int_neurons, mem_neurons, dimensions, input_scale, forget_rate, step_size, diff_gain)
		t2 = transform_net(int_neurons, mem_neurons, dimensions, input_scale, forget_rate, step_size, diff_gain)
		t3 = transform_net(int_neurons, mem_neurons, dimensions, input_scale, forget_rate, step_size, diff_gain)
		t4 = transform_net(int_neurons, mem_neurons, dimensions, input_scale, forget_rate, step_size, diff_gain)

		nengo.Connection(s_t.input, t1.mem_input.input)
		nengo.Connection(s_t.input, t2.mem_input.input)
		nengo.Connection(s_t.input, t3.mem_input.input)
		nengo.Connection(s_t.input, t4.mem_input.input)

		nengo.Connection(t1.transform.output, s_t.output[0:dimensions])
		nengo.Connection(t2.transform.output, s_t.output[dimensions:2*dimensions])
		nengo.Connection(t3.transform.output, s_t.output[2*dimensions:3*dimensions])
		nengo.Connection(t4.transform.output, s_t.output[3*dimensions:4*dimensions])

		nengo.Connection(s_t.gate[0]. t1.mem_input.gate)
		nengo.Connection(s_t.gate[1]. t2.mem_input.gate)
		nengo.Connection(s_t.gate[2]. t3.mem_input.gate)
		nengo.Connection(s_t.gate[3]. t4.mem_input.gate)

	return s_t