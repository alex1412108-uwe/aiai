import random
import pprint
random.seed
pp=pprint.PrettyPrinter(indent=4)

pool_gene={}


def main():
	global pp
	global pool_gene
	#pool_size=input("enter the pool size\n")
	#length_gene=input("enter the gene length\n")
	initialize_gene_pool()#pool_size, length_gene)
	pp.pprint(pool_gene)
	pp.pprint(sum_of_dict_elements(pool_gene, "fitness"))

	#roulette_wheel_selection()


def initialize_gene_pool(pool_size=5, length_gene=3):
	for member in range(0,pool_size):
		value_gene={}
		value_member={}
		for gene in range(0,length_gene):
			value_gene[gene]=random.randint(0,1)
		value_fitness=sum(value_gene.values())
		value_member["fitness"]=value_fitness
		value_member["gene"]=value_gene
		pool_gene[member]=value_member

def roulette_wheel_selection():
	global pp
	global pool_gene
	current_fitness_total=0
	for member, value in pool_gene.items():
		current_fitness_total=current_fitness_total+pool_gene[member]["fitness"]
	pp.pprint(current_fitness_total)

def sum_of_dict_elements(dictionary, element):
	current_total=0
	for member, value in pool_gene.items():
		current_total=current_total+dictionary[member][element]
	return current_total

main()