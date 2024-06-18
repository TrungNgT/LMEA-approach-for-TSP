import random

def OX(parent1, parent2):
    prompt = '{parent1 = ' + f"{parent1}, parent2 = {parent2}" + '} '

    size=len(parent1)
    # Step 1: Select random crossover range
    start, end = sorted(random.sample(range(1, size-2), 2))   # Avoid the first and last gene

    # Step 2: Create proto-child by inheriting the selected range from its parent
    child1 = [None]*len(parent1)
    child1[start:end] = parent1[start:end]

    child2 = [None]*len(parent2)
    child2[start:end] = parent2[start:end]
    
    loc1 = child1.copy()
    loc2 = child2.copy()

    # Step 3: Fill in remaining positions in child1 with other cities in parent2
    for i in range(len(parent2)):
        if parent2[i] not in child1:
            child1[child1.index(None)] = parent2[i]

    #Step 4: Fill in remaining positions in child2 with other cities in parent1
    for i in range(len(parent1)):
        if parent1[i] not in child2:
            child2[child2.index(None)] = parent1[i]

    prompt += ('{child1: ' + f"{child1}, child2: {child2}" + '} ' + 'Explanation: {Step 1: Select random crossover range in both 2 parents: ' + f"(start={start}, end={end}); ")
    prompt += ('Step 2: Create proto-child by inheriting the selected range from its parent: ' + f"(child1={loc1}, child2={loc2}); ")
    prompt += ('Step 3: Fill in remaining positions in child1 with other cities in parent2: ' + f"child1={child1}; ")
    prompt += ('Step 4: Fill in remaining positions in child2 with other cities in parent1: ' + f"child2={child2}" + '}\n')
    
    print(prompt)
    return child1, child2


# Define parent genes
parent1 = [10, 1, 14, 3, 12, 6, 4, 7, 9, 11, 8, 2, 13, 5]
parent2 = [10, 11, 4, 12, 14, 5, 9, 1, 8, 3, 6, 7, 13, 2]

# Perform crossover
child1, child2 = OX(parent1, parent2)








#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def order_one_crossover(parent1, parent2):
    """
    Applies Order One Crossover (OX1) to two parent chromosomes.

    Args:
        parent1 (list): First parent chromosome (list of integers).
        parent2 (list): Second parent chromosome (list of integers).

    Returns:
        tuple: Two offspring chromosomes resulting from OX1.
    """
    # Choose a random crossover point
    crossover_point = random.randint(0, len(parent1) - 1)

    # Initialize offspring with placeholders
    offspring1 = [None] * len(parent1)
    offspring2 = [None] * len(parent2)

    # Copy the segment from parent1 to offspring1
    offspring1[crossover_point:] = parent1[crossover_point:]
    offspring2[crossover_point:] = parent2[crossover_point:]

    # Fill in remaining positions in offspring2
    for i in range(len(parent2)):
        if parent2[i] not in offspring1:
            offspring1[offspring1.index(None)] = parent2[i]

    # Fill in remaining positions in offspring1
    for i in range(len(parent1)):
        if parent1[i] not in offspring2:
            offspring2[offspring2.index(None)] = parent1[i]

    return offspring1, offspring2

# Example usage:
'''
parent1 = [10, 1, 14, 3, 12, 6, 4, 7, 9, 11, 8, 2, 13, 5]
parent2 = [10, 11, 4, 12, 14, 5, 9, 1, 8, 3, 6, 7, 13, 2]
offspring1, offspring2 = order_one_crossover(parent1, parent2)
print("Offspring 1:", offspring1)
print("Offspring 2:", offspring2)
'''
