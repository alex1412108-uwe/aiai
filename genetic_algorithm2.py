
#####windows setup to get graphing working, currently doesnt work########################################################
#getting matplotlib working from: http://stackoverflow.com/questions/18280436/importerror-matplotlib-requires-dateutil  #
#numpy (numpy-MKL-1.8.0.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy                     #
#matplotlib (matplotlib-1.3.1.win-amd64-py3.3.exe) from: http://matplotlib.org/downloads.html                           #
#dateutil (python-dateutil-2.2.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-dateutil    #
#pytz (pytz-2013.8.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pytz                           #
#pyparsing (pyparsing-2.0.1.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyparsing             #
#six (six-1.4.1.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#six                               #
########################################################################################################################3
import random
import pprint
import scipy
import matplotlib.pyplot as plt

random.seed

def main():
    global pp
    pp = pprint.PrettyPrinter(indent = 4)
    ax = plt.subplot(111)

    pool_size = 50#input("enter the pool size\n") #must be even
    gene_length = 50#input("enter the gene length\n")
    parents_number = pool_size #must be even
    mutation_rate = .01 #percentage as a decimal

    pool_gene=initialize_gene_pool(pool_size, gene_length)
    #pp.pprint(pool_gene)
    current_fitness_total = sum_of_fitness(pool_gene)
    pp.pprint(current_fitness_total)

    highest_fitness_total=0
    optimal_found=False
    for i in range(0,100):
        parents_gene = roulette_wheel_selection(pool_gene, pool_size, gene_length, parents_number)
        #pp.pprint(parents_gene)
        children_gene = single_point_crossover(parents_gene, pool_size, gene_length, parents_number)
        #pp.pprint(children_gene)
        mutated_gene = mutation(children_gene, pool_size, gene_length, mutation_rate)
        #pp.pprint(mutated_gene)
        pool_gene = mutated_gene
        #pp.pprint(pool_gene)
        pool_gene = fitness_of_members(pool_gene, pool_size, gene_length)
        #pp.pprint(pool_gene)
        current_fitness_total = sum_of_fitness(pool_gene)
        pp.pprint(current_fitness_total)

        highest_fitness_total = current_fitness_total if current_fitness_total > highest_fitness_total else highest_fitness_total
        
        ax.scatter(i,current_fitness_total, s=40, c='b', marker='s', faceted=False)
        if current_fitness_total == gene_length * pool_size:
            print("")
            print("generations taken="+str(i))
            optimal_found=True
            break
    if optimal_found == False:
        print('no optimal found')
    print("highest fitness total=" + str(highest_fitness_total))
    print("fitness goal=" + str(gene_length*pool_size))
    #settings
    plt.grid(True)
    #label graph
    plt.xlabel(r"generation", fontsize = 12)
    plt.ylabel(r"fitness", fontsize = 12)
    # Produce output
    plt.savefig('plot.png', dpi=96)

def initialize_gene_pool(pool_size = 2, gene_length = 2):
    pool_gene = {}
    for member in range(0,pool_size):
        value_gene = list(range(gene_length))
        value_member = {}
        for gene in range(0,gene_length):
            value_gene[gene] = random.randint(0,1)
        value_fitness = sum(value_gene)
        value_member["gene"] = value_gene
        value_member["fitness"] = value_fitness
        pool_gene[member] = value_member
    return pool_gene


def roulette_wheel_selection(pool_gene, pool_size, gene_length, parents_number):
    parents_gene = {}
    current_fitness_total = sum_of_fitness(pool_gene)
    for parent in range(0,parents_number):
        cutoff = random.randint(0,current_fitness_total)
        fitness_sum = 0 #resets the fitness counter
        for member in range(0,pool_size):
            fitness_sum = fitness_sum + pool_gene[member]["fitness"] #increases the fitness counter by the current members fitness
            if fitness_sum >= cutoff: 
                parents_gene[parent] = pool_gene[member]
                break
    return parents_gene

def single_point_crossover(parents_gene, pool_size, gene_length, parents_number):
    children_gene = {}

    for member in range(0, parents_number,2):
        gene1 = parents_gene[member]["gene"]
        gene2 = parents_gene[member + 1]["gene"]

        crossover_point = random.randint(1,gene_length-1)

        gene1_child = gene1[:crossover_point] + gene2[crossover_point:]
        gene2_child = gene2[:crossover_point] + gene1[crossover_point:]

        children_gene[member] = {"gene":gene1_child}
        children_gene[member + 1] = {"gene":gene2_child}

    return children_gene


def mutation(children_gene, pool_size, gene_length, mutation_rate):
    mutated_gene = {}

    for member in range(0,pool_size):
        mutated_gene_list = list(range(gene_length))
        for gene in range (0,gene_length):
            if random.random() < mutation_rate: #random.random returns a float between 0 and 1
                mutated_gene_list[gene] = children_gene[member]["gene"][gene] ^ 1 #inverts the gene
            else:
                mutated_gene_list[gene] = children_gene[member]["gene"][gene] #leaves gene the same
        mutated_gene[member] = {"gene":mutated_gene_list}
    return mutated_gene

def fitness_of_members(pool_gene, pool_size, gene_length):
    for member in range(0,pool_size):
        pool_gene[member]["fitness"] = sum(pool_gene[member]["gene"])
    return pool_gene


def sum_of_fitness(pool_gene):
    current_total = 0
    for member, value in pool_gene.items():
        current_total = current_total + pool_gene[member]["fitness"]
    return current_total


if __name__ == "__main__":
    main()
