# entropy-based measure

import random

import math

e = 2.71828

thres_hold = math.log(5) / math.log(e)

popu = []

pop_si = 40

n_n = 14

while(len(popu) < pop_si/5) :
    permutation =  list(random.sample(range(1, n_n + 1), n_n))
    popu.append(permutation)

popu.extend(popu)
popu.extend(popu)
popu.extend(popu)
popu.extend(popu)

'''

population = []

pop_size = 40

n = 14

e = 2.71828

a = 3

thres_hold = math.log(5) / math.log(e)

while(len(population) < pop_size/5) :
    permutation =  list(random.sample(range(1, n + 1), n))
    population.append(permutation)

population.extend(population)
population.extend(population)
population.extend(population)
population.extend(population)

count = 0

def pr(i: int, c:int) :
    na = 0
    for j in range(pop_size):
        if (population[j][i] == c):
            na += 1
    
    return (na / pop_size)

index_list = []

for i in range(n) :

    H = 0
    for c in range(1, n+1):
        prob = pr(i, c)
        if prob != 0.0:
            H += prob * (math.log(prob) / math.log(e))

    H = -H
    if (H <= thres_hold):
        count += 1
        index_list.append(i)
    else:
        print(f"vị trí không thỏa {i} có H = {H}")

print(count)
    
if (count >= n/a):
    print("diversity too low")

else:
    print("good abundant!")

print("danh sách các vị trí thỏa mãn H(i) <= threshold: ")
print(index_list)

print("Kiểm chứng các vị trí có thỏa mãn: ")

for h in index_list:
    n_list = []
    for s in range(8):
        n_list.append(population[s][h])
    print(n_list)

not_valid_indx = []
for j in range(n):
    if j not in index_list:
        not_valid_indx.append(j)

print("danh sách các vị trí không thỏa mãn threshold: ")
print(not_valid_indx)

print("Kiểm chứng các vị trí không thỏa mãn H(i) <= threshold tức là tại vị trí _i có nhiều hơn e^thresdhold: ")

for j in not_valid_indx:
    new_list = []
    for t in range(8):
        new_list.append(population[t][j])
    print(new_list)

'''

def pr(i: int, c:int, pop_size: int, population: list) :
    na = 0
    for j in range(pop_size):
        if (population[j][i] == c):
            na += 1
    
    return (na / pop_size)

def entropy_measuring(population: list, pop_size: int, n: int, a: int, exp_thsh: int):
    thres_hold = math.log(exp_thsh) / math.log(e)
    count = 0
    index_list = []
    
    for i in range(n) :
        H = 0
        for c in range(1, n+1):
            prob = pr(i, c, pop_size, population)
        
            if prob != 0.0:
                H += prob * (math.log(prob) / math.log(e))

        H = -H

        if (H <= thres_hold):
            count += 1
            index_list.append(i)
        else:
            print(f"Vi tri khong thoa {i} khi so sanh voi entropy <= ln(?) co H = {H}")
    
    print(f"count = {count}")
        
    
    if count >= n/a:
        return "too_low"
    else:
        return "good"

print(entropy_measuring(population=popu, pop_size=pop_si, n=14, a=2, exp_thsh=7))
