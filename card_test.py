from cards import Card
import itertools
import ipdb

colours = ["GREEN", "RED", "YELLOW", "BLUE"]
numbers = ["ONE", "TWO", "THREE", "FOUR"]
shapes = ["SQUARE", "CIRCLE", "TRIANGLE", "PLUS"]
# create a deck full of cards
deck = []
for card in itertools.product(colours, numbers, shapes):
	deck.append(Card(*card))

ipdb.set_trace()