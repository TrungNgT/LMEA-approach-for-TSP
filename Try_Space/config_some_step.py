import time

from support import *
from what_ever_to_try import *
from edAdj_instance import *

from instance import *



import google.generativeai as genai


genai.configure(api_key='_YOUR_API_KEY_')

model = genai.GenerativeModel(model_name='gemini-pro')

'''
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# TODO(developer): Update and un-comment below line
project_id = "_PRJ_ID_"

vertexai.init(project=project_id, location="us-central1")

model = GenerativeModel(model_name="gemini-1.5-pro-001")
'''
#-------------------------------------------------------------------------------------------------------------------------
# some prompts formats
# prompt for crossover:
description = 'You are given a list of points with coordinates: {' + list2str() + '}. A solution is a trace, with the shortest possible length, that traveles each point exactly once.\n'
description += 'You will be given 2 parent solutions, your task is ONLY use one of the 2 Crossover operators provided below on the 2 parent solutions and generate 2 new Offsprings.'

in_context = 'Below are some previous traces and their lengths. The traces are arranged in descending order based on their lengths, where lower values are better.\n'
# remember to reduce N compare to the last algo

in_context += 'Now, there are Python code and some examples of the first Crossover operator. The examples consist of 2 parent traces and 2 new generated traces with explanations:\n'
in_context += ('import random \n def first_operator(parent1, parent2): \n size = len(parent1) \n #Step 1: Select random crossover range in both 2 parents, avoid the first and last gene \n start, end = sorted(random.sample(range(1, size-2), 2)) \n #Step 2: Create offspring by exchanging the selected range \n child1 = parent1[:start] + parent2[start:end] + parent1[end:] \n child2 = parent2[:start] + parent1[start:end] + parent2[end:] \n #Step 3: Determine the mapping relationship to legalize offspring \n mapping1 = {parent2[i]: parent1[i] for i in range(start, end)' + '}\n' + 'mapping 2 = {parent1[i]: parent2[i] for i in range(start, end)' + '}\n' + '#Step 4: Legalize children with the mapping relationship\n for i in list(range(start)) + list(range(end, size)): \n if child1[i] in mapping1:\n while child1[i] in mapping1: \n child1[i] = mapping1[child1[i]] \n if child2[i] in mapping2:\n while child2[i] in mapping2: \n child2[i] = mapping[child2[i]]\n return (child1, child2) \n return child1, child2 \n')
in_context += '{parent1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], parent2 = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10, 13, 11, 14, 12]} {Offspring 1: [1, 5, 3, 7, 9, 2, 4, 6, 8, 10, 11, 12, 13, 14], Offspring 2: [1, 3, 2, 4, 5, 6, 7, 8, 9, 10, 13, 11, 14, 12]} Explanations: {Step 1: Select random crossover range in both 2 parents: (start=4, end=9); Step 2: Create offspring by exchanging the selected range: (child1=[1, 2, 3, 4, 9, 2, 4, 6, 8, 10, 11, 12, 13, 14], child2=[1, 3, 5, 7, 5, 6, 7, 8, 9, 10, 13, 11, 14, 12]); Step 3: Determine the mapping relationship to legalize offspring: (mapping1={9: 5, 2: 6, 4: 7, 6: 8, 8: 9}, mapping2={5: 9, 6: 2, 7: 4, 8: 6, 9: 8}); Step 4: Legalize children with the mapping relationsip and receive 2 result offsprings as shown.}\n'
in_context += '{parent1 = [14, 12, 13, 11, 9, 8, 10, 6, 5, 7, 2, 4, 3, 1], parent2 = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10, 13, 11, 14, 12]} {Offspring 1: [14, 12, 13, 11, 9, 8, 10, 6, 5, 7, 2, 4, 3, 1], Offspring 2: [1, 3, 5, 7, 9, 2, 4, 6, 8, 10, 13, 11, 14, 12]} Explanations: {Step 1: Select random crossover range in both 2 parents: (start=4, end=5); Step 2: Create offspring by exchanging the selected range: (child1=[14, 12, 13, 11, 9, 8, 10, 6, 5, 7, 2, 4, 3, 1], child2=[1, 3, 5, 7, 9, 2, 4, 6, 8, 10, 13, 11, 14, 12]); Step 3: Determine the mapping relationship to legalize offspring: (mapping1={9: 9}, mapping2={9: 9}); Step 4: Legalize children with the mapping relationsip and receive 2 result offsprings as shown.}\n'
in_context += '{parent1 = [14, 12, 13, 11, 9, 8, 10, 6, 5, 7, 2, 4, 3, 1], parent2 = [14, 12, 13, 11, 9, 2, 4, 6, 8, 10, 3, 7, 5, 1]} {Offspring 1: [14, 12, 13, 11, 9, 8, 10, 6, 5, 7, 2, 4, 3, 1], Offspring 2: [14, 12, 13, 11, 9, 2, 4, 6, 8, 10, 3, 7, 5, 1]} Explanations: {Step 1: Select random crossover range in both 2 parents: (start=1, end=3); Step 2: Create offspring by exchanging the selected range: (child1=[14, 12, 13, 11, 9, 8, 10, 6, 5, 7, 2, 4, 3, 1], child2=[14, 12, 13, 11, 9, 2, 4, 6, 8, 10, 3, 7, 5, 1]); Step 3: Determine the mapping relationship to legalize offspring: (mapping1={12: 12, 13: 13}, mapping2={12: 12, 13: 13}); Step 4: Legalize children with the mapping relationsip and receive 2 result offsprings as shown.}\n'

in_context += 'Now, there are Python code and some examples of the second Crossover operator. The examples consist of 2 parent traces and 2 new generated traces with explanations:\n'
in_context += 'import random \n def second_operator(parent1, parent2): \n size = len(parent1) \n #Step 1: Select random crossover range in both 2 parents, avoid the first and last gene \n start, end = sorted(random.sample(range(1, size-2), 2)) \n # Step 2: Create proto-child by inheriting the selected range from its parent \n child1 = [None]*len(parent1) \n child1[start:end] = parent1[start:end] \n child2 = [None]*len(parent2) \n child2[start:end] = parent2[start:end] \n #Step 3: Fill in remaining positions in child1 with other cities in parent2 \n for i in range(len(parent2)):\n if parent2[i] not in child1:\n child1[child1.index(None)] = parent2[i] \n #Step 4: Fill in remaining positions in child2 with other cities in parent1: \n for i in range(len(parent1)):\n if parent1[i] not in child2:\n child2[child2.index(None)] = parent1[i] \n return child1, child2 \n'
in_context += '{parent1 = [1, 7, 4, 3, 14, 13, 9, 6, 10, 5, 2, 11, 12, 8], parent2 = [7, 9, 1, 13, 11, 10, 8, 2, 4, 14, 5, 3, 6, 12]} {child1: [7, 9, 1, 13, 11, 8, 4, 14, 10, 5, 2, 3, 6, 12], child2: [1, 7, 3, 13, 9, 6, 10, 2, 4, 14, 5, 11, 12, 8]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=8, end=11); Step 2: Create proto-child by inheriting the selected range from its parent: (child1=[None, None, None, None, None, None, None, None, 10, 5, 2, None, None, None], child2=[None, None, None, None, None, None, None, None, 4, 14, 5, None, None, None]); Step 3: Fill in remaining positions in child1 with other cities in parent2: child1=[7, 9, 1, 13, 11, 8, 4, 14, 10, 5, 2, 3, 6, 12]; Step 4: Fill in remaining positions in child2 with other cities in parent1: child2=[1, 7, 3, 13, 9, 6, 10, 2, 4, 14, 5, 11, 12, 8]}\n'
in_context += '{parent1 = [4, 2, 6, 9, 10, 1, 8, 5, 13, 11, 7, 12, 14, 3], parent2 = [13, 3, 4, 2, 7, 9, 8, 1, 10, 5, 6, 14, 12, 11]} {child1: [3, 4, 6, 9, 10, 1, 8, 5, 13, 2, 7, 14, 12, 11], child2: [6, 5, 4, 2, 7, 9, 8, 1, 10, 13, 11, 12, 14, 3]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=2, end=9); Step 2: Create proto-child by inheriting the selected range from its parent: (child1=[None, None, 6, 9, 10, 1, 8, 5, 13, None, None, None, None, None], child2=[None, None, 4, 2, 7, 9, 8, 1, 10, None, None, None, None, None]); Step 3: Fill in remaining positions in child1 with other cities in parent2: child1=[3, 4, 6, 9, 10, 1, 8, 5, 13, 2, 7, 14, 12, 11]; Step 4: Fill in remaining positions in child2 with other cities in parent1: child2=[6, 5, 4, 2, 7, 9, 8, 1, 10, 13, 11, 12, 14, 3]}\n'
in_context += '{parent1 = [10, 1, 14, 3, 12, 6, 4, 7, 9, 11, 8, 2, 13, 5], parent2 = [10, 11, 4, 12, 14, 5, 9, 1, 8, 3, 6, 7, 13, 2]} {child1: [10, 1, 14, 3, 12, 6, 4, 11, 5, 9, 8, 7, 13, 2], child2: [10, 11, 4, 12, 14, 5, 9, 1, 3, 6, 7, 8, 2, 13]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=1, end=7); Step 2: Create proto-child by inheriting the selected range from its parent: (child1=[None, 1, 14, 3, 12, 6, 4, None, None, None, None, None, None, None], child2=[None, 11, 4, 12, 14, 5, 9, None, None, None, None, None, None, None]); Step 3: Fill in remaining positions in child1 with other cities in parent2: child1=[10, 1, 14, 3, 12, 6, 4, 11, 5, 9, 8, 7, 13, 2]; Step 4: Fill in remaining positions in child2 with other cities in parent1: child2=[10, 11, 4, 12, 14, 5, 9, 1, 3, 6, 7, 8, 2, 13]}\n'

task = 'Please follow the instruction step-by-step to generate 2 new offsprings:\n'
task += '1. Now, you are given 2 parent solution traces: '
task2 = '2. You MUST use ONE of the 2 mentioned Crossover Operators with the two traces in Step 1 to generate 2 new Offspring traces.'
task2 += 'Directly give me 2 Offspring traces, bracketed the first Offspring with <Off1> and </Off1> and bracketed the second one with <Off2> and </Off2>. Not any explanation needed.'

#promt for mutation:
mut_prompt = 'You are given a list of points with coordinates: {' + list2str() + '}. A solution is a trace, with the shortest possible length, that traveles each point exactly once.\n'
mut_prompt += 'You now be given 1 solution traces, your task is to do Mutation it and give me the result.\n'
context_learn = 'There are some examples of mutation results shown. The examples consist of the original trace and the mutated trace:\n'
context_learn += '{original trace = [1, 2, 3, 5, 6, 9, 4, 10, 7, 11, 14, 12, 13, 4]} {mutated trace = [1, 2, 10, 4, 9, 6, 5, 3, 7, 11, 14, 12, 13, 4]}\n'
context_learn += '{original trace = [4, 2, 6, 9, 10, 1, 8, 5, 13, 11, 7, 12, 14, 3]} {mutated trace = [4, 11, 6, 9, 10, 1, 8, 5, 13, 2, 3, 14, 12, 7]}\n'
context_learn += '{original trace = [10, 1, 14, 3, 12, 6, 4, 11, 5, 9, 8, 7, 13, 2]} {mutated trace = [3, 14, 1, 10, 9, 6, 4, 11, 5, 12, 2, 13, 7, 8]}\n'

mut_task = 'Please follow the instruction step-by-step to generate new mutated trace:\n'
mut_task += '1. Now, you are given a solution trace: original trace = '
mut_task2 = '2. Muate the given trace and directly give me the result, bracketed it with <mut> and </mut>. Not any explanation needed.'
#-------------------------------------------------------------------------------------------------------------------------

best_cur = 999999999

Pool = randomFirstN(n, N)

best_now = Pool[N-1].length

g = 1


while (g <= G and not check_stuck(best_cur, best_now)) :

    best_cur = Pool[N-1].length

    Pool_sharp = []

    for i in range(1, N+1) :
        
        par1, par2 = tournament_selection(Pool)

        print(f"{i}th pairs of parents in generation {g}:")

        print(f"parent_1: {par1}, parent_2: {par2}")

        if (random.random() < 0.7) :

            crosOv_prompt = description + (in_context + pool2examples(Pool)) + task + parent2str(par1, par2) + task2

            start_time = time.time()

            response = model.generate_content(contents=crosOv_prompt)

            spent_time = time.time() - start_time

            print(f"spent_time for this request: {spent_time}")
            '''
            if spent_time < 30:
                time.sleep(35-spent_time)
            '''

            print(f"crossover of {i}th parents in generation {g}")
            child1, child2 = cut2Offsprings(response.text)
            #print(child1, child2)

            if checkPermu(child1, n):
                Pool_sharp.append(Individual(trace=traceStr2list(child1), length=objective_TSP(traceStr2list(child1))))
            if checkPermu(child2, n):
                Pool_sharp.append(Individual(trace=traceStr2list(child2), length=objective_TSP(traceStr2list(child2))))

            if (random.random() < 0.2) :

                for childStr in [child1, child2]:

                    mutate_prompt = mut_prompt + context_learn + (mut_task + childStr) + mut_task2

                    start_mut_time = time.time()

                    response_mut = model.generate_content(contents=mutate_prompt)

                    spent_time_mut = time.time() - start_mut_time

                    print(f"time for muatating: {spent_time_mut}")

                    sharp_childstr = cutMutated(response_mut.text)

                    if checkPermu(sharp_childstr, n):
                        Pool_sharp.append(Individual(trace=traceStr2list(sharp_childstr), length=objective_TSP(traceStr2list(sharp_childstr))))
                    
                    else:
                        print("!!! Fail mutation process")

        
        print("------------------------------------------------------------------------------")
    
    Pool = updatePool(Pool, Pool_sharp, N)

    best_now = Pool[N-1].length

    print(f"END generation: {g}")
    
    print("#######################################################################################")
    
    g += 1


print(best_now)


        