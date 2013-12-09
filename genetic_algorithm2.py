
#####windows setup to get graphing working, currently doesnt work########################################################
#getting matplotlib working from: http://stackoverflow.com/questions/18280436/importerror-matplotlib-requires-dateutil  #
#numpy (numpy-MKL-1.8.0.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy                     #
#matplotlib (matplotlib-1.3.1.win-amd64-py3.3.exe) from: http://matplotlib.org/downloads.html                           #
#dateutil (python-dateutil-2.2.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#python-dateutil    #
#pytz (pytz-2013.8.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pytz                           #
#pyparsing (pyparsing-2.0.1.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyparsing             #
#six (six-1.4.1.win-amd64-py3.3.exe) from: http://www.lfd.uci.edu/~gohlke/pythonlibs/#six                               #
#########################################################################################################################

#how to use scipy: http://www.loria.fr/~rougier/teaching/matplotlib/#id5

#genetic algorithm by alex thompson

import random
import pprint
import scipy
import matplotlib.pyplot as plt

plt.figure(figsize=(16,6),dpi=100)

random.seed

def main():
    global pp
    pp = pprint.PrettyPrinter(indent = 4)
    #make into one graph with different colors, divide total by 100 to bring it closer to the other results and mention it in the legend
    axgraph = plt.subplot(111)

    #configurable settings
    pool_size = 50#input("enter the pool size\n") #must be even
    gene_length = 50#input("enter the gene length\n")
    parents_number = pool_size #must be even
    tournament_size = 49
    generations = 50
    mutation_rate = .01 #percentage as a decimal
    crossover_rate = .9

    pool_gene = initialize_gene_pool(pool_size, gene_length)
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

        #pp.pprint(pool_gene)
        #parents_gene = roulette_wheel_selection(pool_gene, parents_number, highest_fitness_member)
        #pp.pprint(parents_gene)
        parents_gene = tournament_selection(pool_gene, parents_number, tournament_size, highest_fitness_member)
        #pp.pprint(parents_gene)
        shuffled_gene = shuffle(parents_gene)
        #pp.pprint(shuffled_gene)
        children_gene = single_point_crossover(shuffled_gene, crossover_rate)
        #pp.pprint(children_gene)
        mutated_gene = mutation(children_gene, mutation_rate)
        #pp.pprint(mutated_gene)
        pool_gene = mutated_gene
        #pp.pprint(pool_gene)
        pool_gene = fitness_of_members(pool_gene)
        #pp.pprint(pool_gene)
        current_fitness_total = sum_of_fitness(pool_gene)

        highest_fitness_total = current_fitness_total if current_fitness_total > highest_fitness_total else highest_fitness_total
        
        highest_fitness_member[0] = dict(find_highest_fitness(pool_gene, highest_fitness_member))

        graph_points(i+1,current_fitness_total*.01,'y',axgraph)
        graph_points(i+1,current_fitness_total/pool_size,'g',axgraph)
        graph_points(i+1,highest_fitness_member[0]["fitness"],'b',axgraph)


        if highest_fitness_member[0]["fitness"] == gene_length:
            print("")
            print("generations taken="+str(i+1))
            optimal_found=True
            break
    if optimal_found == False:
        print('no optimal found')
    print("highest fitness member=" + str(highest_fitness_member[0]["fitness"]))
    print("fitness goal=" + str(gene_length))

    #graphing

    #settings
    plt.grid(True)
    #label graphs
    axgraph.set_xlabel(r"generation", fontsize = 12)
    axgraph.set_ylabel(r"fitness", fontsize = 12)
    plt.legend(('total fitness*0.01','mean fitness','best member'), loc = 'lower right')
    #set graph limits
    axgraph.set_xlim(0,generations)
    axgraph.set_ylim(0,gene_length)
    # Produce output
    plt.savefig('graphs.png', dpi=150)
    plt.show()

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
    children_gene = {}
    gene_length=len(shuffled_gene[0]["gene"])

    for member in range(0, len(shuffled_gene),2):
        if random.random() < crossover_rate: #random.random returns a float between 0 and 1
            gene1 = shuffled_gene[member]["gene"]
            gene2 = shuffled_gene[member + 1]["gene"]

            crossover_point = random.randint(1,gene_length-1)

            gene1_child = gene1[:crossover_point] + gene2[crossover_point:]
            gene2_child = gene2[:crossover_point] + gene1[crossover_point:]

            children_gene[member] = {"gene":gene1_child}
            children_gene[member + 1] = {"gene":gene2_child}
        else:
            children_gene[member] = {"gene":shuffled_gene[member]["gene"]}
            children_gene[member + 1] = {"gene":shuffled_gene[member+1]["gene"]}

    return children_gene


def mutation(children_gene, mutation_rate):
    mutated_gene = {}
    pool_size=len(children_gene)
    gene_length=len(children_gene[0]["gene"])
    for member in range(0,pool_size):
        mutated_gene_list = list(range(gene_length))
        for gene in range (0,gene_length):
            if random.random() < mutation_rate: #random.random returns a float between 0 and 1
                mutated_gene_list[gene] = children_gene[member]["gene"][gene] ^ 1 #inverts the gene
            else:
                mutated_gene_list[gene] = children_gene[member]["gene"][gene] #leaves gene the same
        mutated_gene[member] = {"gene":mutated_gene_list}
    return mutated_gene

def fitness_of_members(pool_gene):
    pool_size=len(pool_gene)
    for member in range(0,pool_size):
        pool_gene[member]["fitness"] = sum(pool_gene[member]["gene"])
    return pool_gene


def sum_of_fitness(pool_gene):
    current_total = 0
    for member, value in pool_gene.items():
        current_total = current_total + pool_gene[member]["fitness"]
    return current_total

def graph_points(x,y,color,axgraph):
    axgraph.scatter(x,y, s=40, c=color, marker='s', faceted=False)

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
