#see march 3, 2014 lecture for more details

import csv
import random
import re #regular expressions library

random.seed

def main():
	data=list(datareader())
	random.shuffle(data)
	dataset1=data[:16]
	dataset2=data[17:]
	print dataset1
	print dataset2
	#if re.match
	print initialize_rule_set()


def datareader():
	with open('data1.txt', 'rb') as csvfile:
		datafromfile = list(csv.reader(csvfile, delimiter=' ', quotechar='|'))
		del datafromfile[0]
	return datafromfile
		#for row in datafromfile:
			#print row

def initialize_rule_set(rule_set_size=10, rule_length=5):
    rule_set = {}
    for member in range(0,rule_set_size):
        value_rule = list(range(rule_length))
        value_member = {}
        for rule in range(0,rule_length):
            value_rule[rule] = random.choice(['0','1','[01]'])
        value_fitness = 0
        value_member["rule"] = value_rule
        value_member["fitness"] = value_fitness
        rule_set[member] = value_member
    return rule_set

#def fitness_test():
	#''.join()

main()