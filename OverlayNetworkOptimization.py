#########################################################
#                                                                                                             #
#       Assignment 1: GENETIC ALGORITHM APPLIED TO                      #
#       OVERLAY NETWORK OPTIMIZATION                                           #
#                                                                                                             #
#       Author:  Burugupalli Mohan                                                         #
#                                                                                                            #
#       Student ID:  1252860                                                                   #
#                                                                                                            #
#       Please DO NOT publish your implemented code                        #
#       for example on GitHub				              #
#                                                                                                            #
#########################################################
# In[1] :
import random
import numpy as np
import matplotlib.pyplot as plt
from random import random
from random import seed

#########################################################
# PARAMETERS                                                                                      #
#########################################################
popSize = 100
chromLength = 300
iteration_max = 200
crossover_rate = 0.2
mutation_rate = 0.2

fitness = np.empty([popSize]) 
costVector = np.empty([chromLength])

#########################################################
# Load network                                                                                       #
#########################################################

def loadNetwork():
    fname = "network.txt"
    input = np.loadtxt(fname)
    for i in range(0, chromLength):
        costVector[i] = input[i][2]
		

#########################################################
# FITNESS EVALUATION                                                                          #
#########################################################
def evaluateFitness(chromosome, best):
    costFullyConnectedNetwork = 30098.059999999983
    fitness_total = 0.0
    fitness_average = 0.0

    for i in range(0, popSize):
        fitness[i] = 0

    for i in range(0, popSize):
        cost = 0
        for j in range(0, chromLength):
            if chromosome[i, j] == 1:
                cost = cost + costVector[j]
        fitness[i] = 1 - (cost / costFullyConnectedNetwork)
        fitness_total = fitness_total + fitness[i]
    fitness_average = fitness_total / popSize

    for i in range(0, popSize):
        if fitness[i] >= best:
            best = fitness[i]
        
    return best, fitness_average


#########################################################
# PERFORMANCE GRAPH                                                                       #
#########################################################
def plotChart(best, avg):
    plt.plot(best, label='best')
    plt.plot(avg, label='average')
    plt.ylabel('Fitness')
    plt.xlabel('Iterations')
    plt.legend()
    plt.xlim(1, iteration_max - 1)
    plt.ylim(0.0, 1.0)
    plt.show()
	
	
##########################################################################################
# RANDOM SELECTION OF POPULATION FOR CROSSOVER USING TOURNAMENT SELECTION METHOD            #
##########################################################################################

def selection_Ofparents(network_links, popSize):
    x = 0
    y = network_links[0]
    z = 0
    while x < 2:
        a = np.random.randint(0, popSize)
        b = np.random.randint(0, popSize)
        evaluateFitness(network_links,popSize)
        fitp1 = fitness[a]
        fitp2 = fitness[b]
        if (x == 0):
            if fitp2 <= fitp1:
                y = a
            else:
                y = b
        else:
            if fitp2 <= fitp1:
                z = a
            else:
                z = b
            x += 1
        return y, z

#########################################################
# CROSSOVER                                                                                         #
#########################################################
def crossover(p1, p2, chromLength):
    k = np.random.randint(0,2)
    if k < crossover_rate:
        b = np.random.randint(0, chromLength)
        a = np.random.randint(0, chromLength)
        if  a <= b:
            b, a = a, b
        else:
            b = b
            a = a
        p1[b:a] = p2[b:a]
        p2[b:a] = p1[b:a]
        return p1, p2
    else:
        return p1, p2

#########################################################
# MUTATION                                                                                          #
#########################################################

def mutation(p1, p2, chromLength):
    seed(1)
    k = np.random.randint(0,8)
    if mutation_rate >= k:
        cutover = np.random.randint(0, chromLength)
        if p1[cutover] == 0:
            p1[cutover] = 1
        else:
            p1[cutover] = 0
        if p2[cutover] == 0:
            p2[cutover] = 1
        else:
            p2[cutover] = 0
        return p1, p2
    else:
        return p1, p2

#########################################################
# MAIN                                                                                                   #
#########################################################
if __name__ == '__main__':
    best=0.0
    average=0.0
    iteration=0
    bestM = np.empty([iteration_max],dtype=np.float32)
    averageM = np.empty([iteration_max],dtype=np.float32)
    print("GENETIC ALGORITHM APPLIED TO OVERLAY NETWORK OPTIMIZATION")
    network_links=(popSize,chromLength)
    network_links=np.random.randint(2,size=network_links)
    loadNetwork()
    best,fitness_average=evaluateFitness(network_links,best)
    setarr=[]
    while (iteration<=iteration_max-1):
        i=0
        best=0.0
        average=0.0
        setarr=[]
        while i<50:  
            p1,p2=selection_Ofparents(network_links,popSize)
            overlay1=network_links[p1]
            overlay2=network_links[p2]
            overlay1,overlay2=crossover(overlay1,overlay2,chromLength)
            overlay1,overlay2=mutation(overlay1,overlay2,chromLength)
            setarr.append(overlay1)
            setarr.append(overlay2)
            i+=1
        network_links=(np.array(setarr))
        best,fitness_average=evaluateFitness(network_links,best)
        bestM[iteration] = best
        averageM[iteration] = fitness_average
        iteration=iteration+1
    plotChart(bestM,averageM)

