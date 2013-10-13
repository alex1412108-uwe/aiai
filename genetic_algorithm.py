import random
import pprint
random.seed
pp=pprint.PrettyPrinter(indent=4)

pool_gene={}


def main():
	global pool_gene
	#pool_size=input("enter the pool size\n")
	#length_gene=input("enter the gene length\n")
	initialize_gene_pool()#pool_size, length_gene)
	pp.pprint(pool_gene)

def initialize_gene_pool(pool_size=4, length_gene=3):
	for member in range(0,pool_size):
		value_gene={}
		value_member={}
		for gene in range(0,length_gene):
			value_gene[gene]=random.randint(0,1)
		value_fitness=sum(value_gene.values())
		value_member["fitness"]=value_fitness
		value_member["gene"]=value_gene
		pool_gene[member]=value_member

main()