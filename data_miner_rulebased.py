#see march 3, 2014 lecture for more details
#needs to learn from the first half to solve for the second half
#input(first column) needs to result in the output (second column)

import csv
import random
import re #regular expressions library
import pprint
import scipy
import matplotlib.pyplot as plt

random.seed

plt.figure(figsize=(16,6),dpi=115)

def main():
	global pp
	pp = pprint.PrettyPrinter(indent = 2)
	data = list(datareader())
	random.shuffle(data)
	dataset1 = data[:16]
	dataset2 = data[17:]
	genetic_algorithm(30, len(data[0][0]), 100, dataset1)


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
			value_rule[rule] = random.choice(["0","1","[01]"])
		value_fitness = 0
		value_member["gene"] = value_rule
		value_member["result"] = 1#random.choice([0,1])
		value_member["fitness"] = value_fitness
		rule_set[member] = value_member
	return rule_set

def fitness_test(rule_set, dataset):
	global pp
	pp = pprint.PrettyPrinter(indent = 1)
	for key, member in rule_set.items():
		fitness = 1
		rule_string = ''.join(member["gene"])
		for data in dataset:
			# if member["result"] == int(data[1]):
			# 	fitness += 0
			if re.match(rule_string, data[0]):
				if int(data[1]) == 0:
					fitness -= 1
				elif int(data[1]) == 1:
					fitness += 1
				else:
					print "error"
		rule_set[key]["fitness"] = fitness
	return rule_set

def genetic_algorithm(pool_size=0, gene_length=0, generations=0, dataset1=0):
	global pp
	pp = pprint.PrettyPrinter(indent = 1)
	#make into one graph with different colors, divide total by 100 to bring it closer to the other results and mention it in the legend
	axgraph = plt.subplot(111)

	#configurable settings
	#pool size must be even
	parents_number = pool_size #must be even
	#tournament_size = 15
	mutation_rate = .05 #percentage as a decimal
	crossover_rate = .5

	pool_gene = initialize_rule_set(pool_size, gene_length)
	#pp.pprint(pool_gene)
	pool_gene = fitness_test(pool_gene, dataset1)
	#pp.pprint(pool_gene)
	current_fitness_total = sum_of_fitness(pool_gene)

	highest_fitness_total = 0
	highest_fitness_member={}
	highest_fitness_member[0] = {"fitness":0}
	highest_fitness_member[0] = dict(find_highest_fitness(pool_gene, highest_fitness_member))

	graph_points(0,current_fitness_total*.01,'y',axgraph)
	graph_points(0,current_fitness_total/pool_size,'g',axgraph)
	graph_points(0,highest_fitness_member[0]["fitness"],'b',axgraph)
	
	optimal_found = False
	for i in range(0,generations):

		pp.pprint(pool_gene)
		parents_gene = roulette_wheel_selection(pool_gene, parents_number, highest_fitness_member)
		#pp.pprint(parents_gene)
		#parents_gene = tournament_selection(pool_gene, parents_number, tournament_size, highest_fitness_member)
		#pp.pprint(parents_gene)
		shuffled_gene = shuffle(parents_gene)
		#pp.pprint(shuffled_gene)
		children_gene = single_point_crossover(shuffled_gene, crossover_rate)
		#pp.pprint(children_gene)
		mutated_gene = mutation(children_gene, mutation_rate)
		#pp.pprint(mutated_gene)
		pool_gene = mutated_gene
		#pp.pprint(pool_gene)
		pool_gene = fitness_test(pool_gene, dataset1)
		#pp.pprint(pool_gene)
		current_fitness_total = sum_of_fitness(pool_gene)

		highest_fitness_total = current_fitness_total if current_fitness_total > highest_fitness_total else highest_fitness_total
		
		highest_fitness_member[0] = dict(find_highest_fitness(pool_gene, highest_fitness_member))

		graph_points(i+1,current_fitness_total*.01,'y',axgraph)
		graph_points(i+1,current_fitness_total/pool_size,'g',axgraph)
		graph_points(i+1,highest_fitness_member[0]["fitness"],'b',axgraph)


		if highest_fitness_member[0]["fitness"] == gene_length:
			#print("")
			print("generations taken="+str(i+1))
			optimal_found=True
			break
	if optimal_found == False:
		print('no optimal found')
	#print("highest fitness member=" + str(highest_fitness_member[0]["fitness"]))
	#print("fitness goal=" + str(gene_length))

	pp.pprint(pool_gene)
	#print highest_fitness_member

	#graphing

	#settings
	plt.grid(True)
	#label graphs
	axgraph.set_xlabel(r"generation", fontsize = 12)
	axgraph.set_ylabel(r"fitness", fontsize = 12)
	plt.legend(('total fitness*0.01','mean fitness','best member'), loc = 'upper left')
	#set graph limits
	#axgraph.set_xlim(0,i)
	axgraph.set_ylim(0,10)
	# Produce output
	#plt.savefig('graphs.png', dpi=150)
	plt.show()
	return i+1

def roulette_wheel_selection(pool_gene, parents_number, highest_fitness_member):
	parents_gene = {}
	pool_size=len(pool_gene)

	current_fitness_total = sum_of_fitness(pool_gene)
	for parent in range(0,parents_number-1):
		cutoff = random.randint(0,current_fitness_total)
		fitness_sum = 0 #resets the fitness counter
		for member in range(0,pool_size):
			fitness_sum = fitness_sum + pool_gene[member]["fitness"] #increases the fitness counter by the current members fitness
			if fitness_sum >= cutoff: 
				parents_gene[parent] = pool_gene[member]
				break
	parents_gene[parents_number-1] = dict(highest_fitness_member[0])
	return parents_gene

def tournament_selection(pool_gene, parents_number, tournament_size, highest_fitness_member):
	parents_gene = {}
	tournament=list(range(tournament_size))
	tournament_winner=0
	tournament_winner_fitness=0
	pool_size=len(pool_gene)

	for parent in range(0,parents_number-1):
		for tournament_member in range(0, tournament_size):
			tournament[tournament_member] = random.randint(0,pool_size-1)
		for tournament_member in tournament:
			if pool_gene[tournament_member]["fitness"] > tournament_winner_fitness:
				tournament_winner_fitness = pool_gene[tournament_member]["fitness"]
				tournament_winner = tournament_member

		parents_gene[parent] = pool_gene[tournament_winner]

	parents_gene[parents_number-1] = dict(highest_fitness_member[0])
	return parents_gene

def shuffle(parents_gene):
	shuffle_gene = {}
	parents_gene_number = len(parents_gene)
	random_list = range(0,parents_gene_number)
	random.shuffle(random_list)
	for member in range(0, parents_gene_number):
		shuffle_gene[member] = dict(parents_gene[random_list[member]])
	return shuffle_gene

def single_point_crossover(shuffled_gene, crossover_rate):
	children_gene = dict(shuffled_gene)
	gene_length=len(shuffled_gene[0]["gene"])

	for member in range(0, len(shuffled_gene),2):
		if random.random() < crossover_rate: #random.random returns a float between 0 and 1
			gene1 = shuffled_gene[member]["gene"]
			gene2 = shuffled_gene[member + 1]["gene"]

			crossover_point = random.randint(1,gene_length-1)

			gene1_child = gene1[:crossover_point] + gene2[crossover_point:]
			gene2_child = gene2[:crossover_point] + gene1[crossover_point:]

			children_gene[member]["gene"] = gene1_child
			children_gene[member + 1]["gene"] = gene2_child
		else:
			children_gene[member]["gene"] = shuffled_gene[member]["gene"]
			children_gene[member + 1]["gene"] = shuffled_gene[member+1]["gene"]
	return children_gene


def mutation(children_gene, mutation_rate):
	mutated_gene = dict(children_gene)
	pool_size=len(children_gene)
	gene_length=len(children_gene[0]["gene"])
	for member in range(0,pool_size):
		mutated_gene_list = list(range(gene_length))
		for gene in range (0,gene_length):
			if random.random() < mutation_rate: #random.random returns a float between 0 and 1
				gene_choice=["0","1","[01]"]
				gene_choice.remove(children_gene[member]["gene"][gene])
				mutated_gene_list[gene] = random.choice(gene_choice) #chooses a random new gene that is not the original
			else:
				mutated_gene_list[gene] = children_gene[member]["gene"][gene] #leaves gene the same
		mutated_gene[member]["gene"] = mutated_gene_list
	return mutated_gene

def sum_of_fitness(pool_gene):
	current_total = 0
	for member, value in pool_gene.items():
		current_total = current_total + pool_gene[member]["fitness"]
	return current_total

def graph_points(x,y,color,axgraph):
	axgraph.scatter(x,y, s=20, c=color, marker='s', edgecolors='none')

def find_highest_fitness(pool_gene, highest_fitness_member):
	highest_fitness_member_current = {}
	for member in range(0,len(pool_gene)):
		if pool_gene[member]["fitness"] > highest_fitness_member[0]["fitness"]:
			highest_fitness_member_current = dict(pool_gene[member])
			highest_fitness_member[0]["fitness"] = pool_gene[member]["fitness"]
	if not any(highest_fitness_member_current):
		highest_fitness_member_current = dict(highest_fitness_member[0])
	return highest_fitness_member_current

if __name__ == "__main__":
	main()