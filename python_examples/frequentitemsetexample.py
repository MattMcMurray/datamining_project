from pymining import itemmining
from pprint import pprint

transactions = (('a', 'b', 'c', 'd', 'e', 'f'), ('a', 'b', 'c', 'd', 'e'), ('a', 'b', 'c', 'e'), ('a', 'b', 'd'))
relim_input = itemmining.get_relim_input(transactions)
report = itemmining.relim(relim_input, min_support=2.8)

pprint(report)

