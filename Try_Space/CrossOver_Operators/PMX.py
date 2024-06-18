import random

def PMX(parent1, parent2):
    size = len(parent1)
    # Step 1: Select crossover range at random
    start, end = sorted(random.sample(range(1, size - 2), 2))  # Avoid the first and last gene (the hive) 
    print(start, end)

    # Step 2: Create offspring by exchanging the selected range
    child1 = parent1[:start] + parent2[start:end] + parent1[end:]
    child2 = parent2[:start] + parent1[start:end] + parent2[end:]
    print(child1, child2)

    # Step 3: Determine the mapping relationship to legalize offspring
    mapping1 = {parent2[i]: parent1[i] for i in range(start, end)}
    mapping2 = {parent1[i]: parent2[i] for i in range(start, end)}
    print(mapping1, mapping2)

    # Step 4: Legalize children with the mapping relationship
    for i in list(range(start)) + list(range(end, size)):
        if child1[i] in mapping1: 
            while child1[i] in mapping1:
                child1[i] = mapping1[child1[i]]
        if child2[i] in mapping2:
            while child2[i] in mapping2:
                child2[i] = mapping2[child2[i]]
    
    return child1, child2


# Define parent genes
parent1 = [14, 12, 13, 11, 9, 8, 10, 6, 5, 7, 2, 4, 3, 1]
parent2 = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10, 13, 11, 14, 12]

# Perform crossover
child1, child2 = PMX(parent1, parent2)

print(child1, child2)