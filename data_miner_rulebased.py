#see march 3, 2014 lecture for more details
#needs to learn from the first half to solve for the second half
#input(first column) needs to result in the output (second column)

import csv
import random
import re #regular expressions library
import pprint

random.seed

def main():
	global pp
	pp = pprint.PrettyPrinter(indent = 2)
	data = list(datareader())
	random.shuffle(data)
	dataset1 = data[:16]
	dataset2 = data[17:]

	rule_set = initialize_rule_set()
	pp.pprint(rule_set)
	rule_set = fitness_test(rule_set, dataset1)
	pp.pprint(rule_set)


def datareader():
	with open('data1.txt', 'rb') as csvfile:
		datafromfile = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))
		del datafromfile[0]
	return datafromfile
		#for row in datafromfile:
			#print row

def initialize_rule_set(rule_set_size=16, rule_length=5):
    rule_set = {}
    for member in range(0,rule_set_size):
        value_rule = list(range(rule_length))
        value_member = {}
        for rule in range(0,rule_length):
            value_rule[rule] = random.choice(['0','1','[01]'])
        value_fitness = 0
        value_member["rule"] = value_rule
        value_member["result"] = random.choice([0,1])
        value_member["fitness"] = value_fitness
        rule_set[member] = value_member
    return rule_set

def fitness_test(rule_set, dataset):
	for key, member in rule_set.items():
		fitness = 0
		rule_string = ''.join(member['rule'])
		for data in dataset:
			if re.match(rule_string, data[0]):
				fitness += 1
				if member['result'] == data[1]:
					fitness += 1
		rule_set[key]['fitness'] = fitness
	return rule_set

main()