import random
import pprint
random.seed
pp=pprint.PrettyPrinter(indent=4)

pool_gene={}


def main():
	global pp
	global pool_gene
	pool_size=10#input("enter the pool size\n")
	gene_length=5#input("enter the gene length\n")
	initialize_gene_pool(pool_size, gene_length)
	roulette_wheel_selection(pool_size, gene_length)
	for member in pool_gene:
		pp.pprint(pool_gene[member]["probability"])
		pp.pprint(pool_gene[member]["probability2"])

def initialize_gene_pool(pool_size=2, gene_length=2):
	for member in range(0,pool_size):
		value_gene={}
		value_member={}
		for gene in range(0,gene_length):
			value_gene[gene]=random.randint(0,1)
		value_fitness=sum(value_gene.values())
		value_member["fitness"]=value_fitness
		value_member["gene"]=value_gene
		pool_gene[member]=value_member

def roulette_wheel_selection(pool_size, gene_length):
	global pp
	global pool_gene
	current_fitness_total=sum_of_dict_elements(pool_gene, "fitness")
	for member in pool_gene:
		pool_gene[member]["probability"]=pool_gene[member]["fitness"]/current_fitness_total
		pool_gene[member]["probability2"]=pool_gene[member]["probability"]*pool_size
	#random.randint(0,current_fitness_total)


def sum_of_dict_elements(dictionary, element):
	current_total=0
	for member, value in pool_gene.items():
		current_total=current_total+dictionary[member][element]
	return current_total

main()