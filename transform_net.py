import nengo
from integrator import ea_integrator

# how to efficiently pass parameters?
def transform_net():
	with nengo.Network(label="transform") as t_n:
		t_n.mem_input = nengo.networks.workingmemory.InputGatedMemory()
		t_n.transform = ea_integrator()
		nengo.Connection(t_n.mem_input.output, t_n.transform.input)
	return t_n
