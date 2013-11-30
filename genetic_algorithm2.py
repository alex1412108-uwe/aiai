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
	parents_number=pool_size
	initialize_gene_pool(pool_size, gene_length)
	pp.pprint(pool_gene)
	print()
	parents_gene=roulette_wheel_selection(pool_size, gene_length, parents_number)
	pp.pprint(parents_gene)
	#single_point_crossover(pool_size, gene_length, parents_gene, parents_number)



def initialize_gene_pool(pool_size=2, gene_length=2):
	for member in range(0,pool_size):
		value_gene=list(range(gene_length))
		value_member={}
		for gene in range(0,gene_length):
			value_gene[gene]=random.randint(0,1)
		value_fitness=sum(value_gene)
		value_member["fitness"]=value_fitness
		value_member["gene"]=value_gene
		pool_gene[member]=value_member

def roulette_wheel_selection(pool_size, gene_length, parents_number):
	global pp
	global pool_gene
	parents_gene={}
	current_fitness_total=sum_of_dict_elements(pool_gene, "fitness")
	print(current_fitness_total)
	for parent in range(0,parents_number):
		cutoff=random.randint(0,current_fitness_total)
		fitness_sum=0 #resets the fitness counter
		for member in range(0,pool_size):
			fitness_sum=fitness_sum+pool_gene[member]["fitness"] #increases the fitness counter by the current members fitness
			if fitness_sum>=cutoff: 
				parents_gene[parent]=member
				break
	return parents_gene


def single_point_crossover(pool_size, gene_length, parents_gene, parents_number):
	global pp
	global pool_gene

	for 
	gene1=[1,1,1,1]
	gene2=[0,0,0,0]

	crossover_point=random.randint(1,len(gene1)-1)

	gene1_child=gene1[:crossover_point]+gene2[crossover_point:]
	gene2_child=gene2[:crossover_point]+gene1[crossover_point:]

	print(crossover_point)
	print(gene1)
	print(gene2)
	print(gene1_child)
	print(gene2_child)

def sum_of_dict_elements(dictionary, element):
	current_total=0
	for member, value in pool_gene.items():
		current_total=current_total+dictionary[member][element]
	return current_total

main()