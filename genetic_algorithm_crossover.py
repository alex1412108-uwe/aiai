import random
random.seed
gene1dict={0:1, 1:1, 2:1, 3:1}
gene2dict={0:0, 1:0, 2:0, 3:0}

gene1=[1,1,1,1]
gene2=[0,0,0,0]

crossover_point=random.randint(1,len(gene1)-1)

gene1_child=gene1[:crossover_point]+gene2[crossover_point:]
gene2_child=gene2[:crossover_point]+gene1[crossover_point:]

print(crossover_point)
print(gene1)
print(gene2)
print(gene1_child)