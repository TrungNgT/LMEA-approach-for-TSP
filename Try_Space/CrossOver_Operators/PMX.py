import random

def PMX(parent1, parent2):
    prompt = '{parent1 = ' + f"{parent1}, parent2 = {parent2}" + '} '

    size = len(parent1)
    # Step 1: Select crossover range at random
    start, end = sorted(random.sample(range(1, size - 2), 2))  # Avoid the first and last gene (the hive) 

    # Step 2: Create offspring by exchanging the selected range
    child1 = parent1[:start] + parent2[start:end] + parent1[end:]
    child2 = parent2[:start] + parent1[start:end] + parent2[end:]
    
    loc1 = child1.copy()
    loc2 = child2.copy()

    # Step 3: Determine the mapping relationship to legalize offspring
    mapping1 = {parent2[i]: parent1[i] for i in range(start, end)}
    mapping2 = {parent1[i]: parent2[i] for i in range(start, end)}

    # Step 4: Legalize children with the mapping relationship
    for i in list(range(start)) + list(range(end, size)):
        if child1[i] in mapping1: 
            while child1[i] in mapping1:
                child1[i] = mapping1[child1[i]]
        if child2[i] in mapping2:
            while child2[i] in mapping2:
                child2[i] = mapping2[child2[i]]

    prompt += ('{child1: ' + f"{child1}, child2: {child2}" + '} ' + 'Explanation: {Step 1: Select random crossover range in both 2 parents: ' + f"(start={start}, end={end}); ")
    prompt += ('Step 2: Create offspring by exchanging the selected range: ' + f"(child1={loc1}, child2={loc2}); ")
    prompt += ('Step 3: Determine the mapping relationship to legalize offspring: ' + f"(mapping1={mapping1}, mapping2={mapping2}); ")
    prompt += ('Step 4: Legalize children with the mapping relationsip and receive 2 result offsprings as shown.}\n')
    
    print(prompt)
    
    return child1, child2


# Define parent genes
parent1 = [20, 1, 4, 6, 2, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, 18, 17, 22]
parent2 = [14, 19, 6, 21, 8, 5, 10, 1, 4, 13, 12, 18, 7, 11, 20, 3, 15, 16, 2, 9, 17, 22]

# Perform crossover
child1, child2 = PMX(parent1, parent2)

#print(child1, child2)