import nengo

def eval_net(p_neurons, e_neurons, dimensions, vocab):
	with nengo.Network(label="eval") as e_n:
		e_n.input = nengo.Node(size_in=dimensions)
		e_n.output = nengo.Node(size_in=4)

		# TODO: ask Nengo experts how to refactor this

		# four evaluation cards
		red_node = nengo.Node(vocab.parse("NUMBER*ONE + SHAPE*TRIANGLE + COLOUR*RED").v)
		green_node = nengo.Node(vocab.parse("NUMBER*TWO + SHAPE*STAR + COLOUR*GREEN").v)
		yellow_node = nengo.Node(vocab.parse("NUMBER*THREE + SHAPE*PLUS + COLOUR*YELLOW").v)
		blue_node = nengo.Node(vocab.parse("NUMBER*FOUR + SHAPE*CIRCLE + COLOUR*BLUE").v)


		# four product networks
		prod_red = nengo.networks.Product(p_neurons, dimensions=dimensions)
		prod_green = nengo.networks.Product(p_neurons, dimensions=dimensions)
		prod_yellow = nengo.networks.Product(p_neurons, dimensions=dimensions)
		prod_blue = nengo.networks.Product(p_neurons, dimensions=dimensions)

		# four results (could these just be nodes?)
		res_red = nengo.Ensemble(e_neurons, 1)
		res_green = nengo.Ensemble(e_neurons, 1)
		res_yellow = nengo.Ensemble(e_neurons, 1)
		res_blue = nengo.Ensemble(e_neurons, 1)

		# connect inputs
		nengo.Connection(e_n.input, prod_red.A, synapse=None)
		nengo.Connection(red_node, prod_red.B, synapse=None)
		nengo.Connection(e_n.input, prod_green.A, synapse=None)
		nengo.Connection(green_node, prod_green.B, synapse=None)
		nengo.Connection(e_n.input, prod_yellow.A, synapse=None)
		nengo.Connection(yellow_node, prod_yellow.B, synapse=None)
		nengo.Connection(e_n.input, prod_blue.A, synapse=None)
		nengo.Connection(blue_node, prod_blue.B, synapse=None)

		# connect outputs
		nengo.Connection(prod_red.output, res_red, transform=nengo.networks.product.dot_product_transform(dimensions))
		nengo.Connection(res_red, e_n.output[0], synapse=0.05)
		nengo.Connection(prod_green.output, res_green, transform=nengo.networks.product.dot_product_transform(dimensions))
		nengo.Connection(res_green, e_n.output[1], synapse=0.05)
		nengo.Connection(prod_yellow.output, res_yellow, transform=nengo.networks.product.dot_product_transform(dimensions))
		nengo.Connection(res_yellow, e_n.output[2], synapse=0.05)
		nengo.Connection(prod_blue.output, res_blue, transform=nengo.networks.product.dot_product_transform(dimensions))
		nengo.Connection(res_blue, e_n.output[3], synapse=0.05)

	# return network
	return e_n