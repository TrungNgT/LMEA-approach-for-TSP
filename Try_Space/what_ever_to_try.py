import time

from support import *
from edAdj_instance import *

from instance import *


def tournament_selection(population: list):
    
    tournament = random.sample(population, 5)

    first_parent = min(tournament, key = compIndiv)

    second_parent = first_parent

    while (second_parent == first_parent) :

        tournament = random.sample(population, 5)

        second_parent = min(tournament, key = compIndiv)
    
    return (first_parent, second_parent)

#population = randomFirstN(n, N)


#parent1, parent2 = tournament_selection(population)

#print(parent2)

