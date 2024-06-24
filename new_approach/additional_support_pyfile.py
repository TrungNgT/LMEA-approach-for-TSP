# %%
from instance_pyfile import *
import random

# %%
def parent2str(par1: Individual, par2: Individual) :
    outString = '{'

    outString += ('parent1 = ' + str(par1.trace) + ', parent2 = ' + str(par2.trace) )

    return outString

# %%
def cut2Offsprings(llmResponse: str) :
    
    child1 = llmResponse[(llmResponse.find("<Off1>")+6) : (llmResponse.find("</Off1>"))]

    child2 = llmResponse[(llmResponse.find("<Off2>")+6) : (llmResponse.find("</Off2>"))]

    return child1, child2

# %%
def cutMutated(llmResponse: str) :
    
    resStr = llmResponse[(llmResponse.find("<mut>")+5) : (llmResponse.find("</mut>"))]

    return resStr

# %%
def tournament_selection(population: list):
    
    tournament = random.sample(population, 5)

    first_parent = min(tournament, key = compIndiv)

    second_parent = first_parent

    while (second_parent == first_parent) :

        tournament = random.sample(population, 5)

        second_parent = min(tournament, key = compIndiv)
    
    return (first_parent, second_parent)


