import nengo
from integrator import ea_integrator

# how to efficiently pass parameters?
def transform_net():
	with nengo.Network(label="transform") as t_n:
		t_n.input = nengo.networks.workingmemory()
		t_n.transform = ea_integrator()
	return t_n
