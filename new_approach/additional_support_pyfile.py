# %%
from instance_pyfile import *
import random
from support_pyfile import randomFirstN as ranFN

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

# %% [markdown]
# 1. Entropy-based diversity measuring
# 

# %%
def uniformTrace(trace: list, n: int) :
    one_idx = -1
    two_idx = -1
    three_idx = -1

    for i in range(n) :
        if trace[i] == 1 :
            one_idx = i
        elif trace[i] == 2 :
            two_idx = i
        elif trace[i] == 3 :
            three_idx = i
        
        if one_idx >= 0 and two_idx >= 0 and three_idx >= 0 :
            break
    
    out_tr = []

    if one_idx < two_idx and two_idx < three_idx :
        if one_idx == 0:
            out_tr = trace
        else :
            out_tr = trace[one_idx:] + trace[:one_idx]
    
    elif one_idx < three_idx and three_idx < two_idx :
        if one_idx == 0:
            out_tr = [trace[one_idx]] + trace[one_idx+1:][::-1]
        else :
            out_tr = trace[:(one_idx+1)][::-1] + trace[one_idx+1:][::-1]
    
    elif two_idx < one_idx and one_idx < three_idx :
        out_tr = trace[:(one_idx+1)][::-1] + trace[one_idx+1:][::-1]

    elif two_idx < three_idx and three_idx < one_idx :
        if one_idx == n-1 :
            out_tr = [trace[one_idx]] + trace[:one_idx]
        else :
            out_tr = trace[one_idx:] + trace[:one_idx]
    
    elif three_idx < one_idx and one_idx < two_idx :
        out_tr = trace[one_idx:] + trace[:one_idx]
    
    elif three_idx < two_idx and two_idx < one_idx :
        if one_idx == n-1 :
            out_tr = [trace[one_idx]] + trace[:one_idx][::-1]
        else :
            out_tr = trace[:one_idx+1][::-1] + trace[one_idx+1:][::-1]

    return out_tr

def Pool2list(population: list):
    popu = []
    for indv in population:
        out_tr = uniformTrace(indv.trace, n=n)
               
        popu.append(out_tr)

    return popu

def pr(i: int, c:int, pop_size: int, popu: list) :
    na = 0
    for j in range(pop_size):
        if (popu[j][i] == c):
            na += 1
    
    return (na / pop_size)

def entropy_measuring(popu: list, pop_size: int, n: int, a: int, exp_thsh: int):                #popu: only traces of individuals
    import math
    
    e = 2.171828
    thres_hold = math.log(exp_thsh) / math.log(e)

    count = 0
    
    for i in range(n) :
        H = 0
        for c in range(1, n+1):
            prob = pr(i, c, pop_size, popu)
        
            if prob != 0.0:
                H += prob * (math.log(prob) / math.log(e))

        H = -H

        if (H <= thres_hold):
            count += 1
        
    
    if count >= n/a:
        return 0
    else:
        return 1

# %% [markdown]
# 2. Re-build population

# %%
def rebuild(population: list, pop_size: int, n: int) :          #population = Pool (list of individuals)
    a_half = int(pop_size/2)
    newPool = ranFN(n, N=a_half)
    
    for indx in range(a_half, pop_size):
        newPool.append(population[indx])
    
    return newPool
    


