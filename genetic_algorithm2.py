import random
import pprint
random.seed
pool_gene={}


def main():
    global pp
    global pool_gene
    pp=pprint.PrettyPrinter(indent=4)
    pool_size=10#input("enter the pool size\n") #must be even
    gene_length=5#input("enter the gene length\n")
    parents_number=pool_size #must be even
    initialize_gene_pool(pool_size, gene_length)
    pp.pprint(pool_gene)
    print()
    parents_gene=roulette_wheel_selection(pool_size, gene_length, parents_number)
    pp.pprint(parents_gene)
    children_gene=single_point_crossover(pool_size, gene_length, parents_gene, parents_number)
    pp.pprint(children_gene)
    mutated_gene=mutation(pool_size, gene_length, parents_gene)
    pp.pprint(mutated_gene)


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
    global pool_gene
    children_gene={}

    for member in range(0, parents_number,2):
        gene1=pool_gene[member]["gene"]
        gene2=pool_gene[member+1]["gene"]

        crossover_point=random.randint(1,gene_length-1)

        gene1_child=gene1[:crossover_point]+gene2[crossover_point:]
        gene2_child=gene2[:crossover_point]+gene1[crossover_point:]

        children_gene[member]={"gene":gene1_child}
        children_gene[member+1]={"gene":gene2_child}
    return children_gene

def mutation(pool_size, gene_length, parents_gene):
    global pool_gene
    for member in range(0,pool_size):
        for gene in range (0,gene_length):
            pass


def sum_of_dict_elements(dictionary, element):
    current_total=0
    for member, value in pool_gene.items():
        current_total=current_total+dictionary[member][element]
    return current_total

main()