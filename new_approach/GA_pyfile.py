# %%
from support_pyfile import *
from additional_support_pyfile import *
from instance_pyfile import *

import time

# %%
import google.generativeai as genai


genai.configure(api_key='AIzaSyBV1xUiqQFJcAAv14dKClxoSR3GYeCLdEs')

model = genai.GenerativeModel(model_name='gemini-pro')

# %%
crx_description = 'You are given a list of points with coordinates: {' + list2str() + '}. A solution is a trace, with the shortest possible length, that traveles each point exactly once.\n'
crx_description += 'You will be given 2 parent solutions, your task is ONLY use one of the 2 Crossover operators provided below on the 2 parent solutions and generate 2 new Offsprings.'

trace_samples = 'Below are some previous traces and their lengths. The traces are arranged in descending order based on their lengths, where lower values are better.\n'
# remember to reduce N compare to the last algo

in_context = 'Now, there are Python code and some examples of the first Crossover operator. The examples consist of 2 parent traces and 2 new generated traces with explanations:\n'
in_context += ('import random \n def first_operator(parent1, parent2): \n size = len(parent1) \n #Step 1: Select random crossover range in both 2 parents, avoid the first and last gene \n start, end = sorted(random.sample(range(1, size-2), 2)) \n #Step 2: Create offspring by exchanging the selected range \n child1 = parent1[:start] + parent2[start:end] + parent1[end:] \n child2 = parent2[:start] + parent1[start:end] + parent2[end:] \n #Step 3: Determine the mapping relationship to legalize offspring \n mapping1 = {parent2[i]: parent1[i] for i in range(start, end)' + '}\n' + 'mapping 2 = {parent1[i]: parent2[i] for i in range(start, end)' + '}\n' + '#Step 4: Legalize children with the mapping relationship\n for i in list(range(start)) + list(range(end, size)): \n if child1[i] in mapping1:\n while child1[i] in mapping1: \n child1[i] = mapping1[child1[i]] \n if child2[i] in mapping2:\n while child2[i] in mapping2: \n child2[i] = mapping[child2[i]]\n return (child1, child2) \n return child1, child2 \n')
in_context += '{parent1 = [10, 5, 3, 19, 18, 11, 2, 14, 20, 12, 7, 21, 8, 6, 1, 17, 4, 9, 15, 13, 16, 22], parent2 = [20, 1, 4, 6, 2, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, 18, 17, 22]} {child1: [10, 1, 4, 6, 2, 11, 18, 14, 20, 12, 7, 21, 8, 19, 5, 17, 3, 9, 15, 13, 16, 22], child2: [20, 5, 3, 19, 18, 11, 8, 10, 6, 7, 9, 1, 12, 21, 13, 15, 16, 14, 4, 2, 17, 22]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=1, end=5); Step 2: Create offspring by exchanging the selected range: (child1=[10, 1, 4, 6, 2, 11, 2, 14, 20, 12, 7, 21, 8, 6, 1, 17, 4, 9, 15, 13, 16, 22], child2=[20, 5, 3, 19, 18, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, 18, 17, 22]); Step 3: Determine the mapping relationship to legalize offspring: (mapping1={1: 5, 4: 3, 6: 19, 2: 18}, mapping2={5: 1, 3: 4, 19: 6, 18: 2}); Step 4: Legalize children with the mapping relationsip and receive 2 result offsprings as shown.}\n'
in_context += '{parent1 = [10, 5, 3, 19, 18, 11, 2, 14, 20, 12, 7, 21, 8, 6, 1, 17, 4, 9, 15, 13, 16, 22], parent2 = [14, 19, 6, 21, 8, 5, 10, 1, 4, 13, 12, 18, 7, 11, 20, 3, 15, 16, 2, 9, 17, 22]} {child1: [2, 3, 6, 21, 8, 5, 10, 1, 4, 13, 12, 18, 7, 11, 20, 17, 14, 9, 15, 19, 16, 22], child2: [4, 13, 3, 19, 18, 11, 2, 14, 20, 12, 7, 21, 8, 6, 1, 5, 15, 16, 10, 9, 17, 22]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=2, end=15); Step 2: Create offspring by exchanging the selected range: (child1=[10, 5, 6, 21, 8, 5, 10, 1, 4, 13, 12, 18, 7, 11, 20, 17, 4, 9, 15, 13, 16, 22], child2=[14, 19, 3, 19, 18, 11, 2, 14, 20, 12, 7, 21, 8, 6, 1, 3, 15, 16, 2, 9, 17, 22]); Step 3: Determine the mapping relationship to legalize offspring: (mapping1={6: 3, 21: 19, 8: 18, 5: 11, 10: 2, 1: 14, 4: 20, 13: 12, 12: 7, 18: 21, 7: 8, 11: 6, 20: 1}, mapping2={3: 6, 19: 21, 18: 8, 11: 5, 2: 10, 14: 1, 20: 4, 12: 13, 7: 12, 21: 18, 8: 7, 6: 11, 1: 20}); Step 4: Legalize children with the mapping relationsip and receive 2 result offsprings as shown.}\n'
in_context += '{parent1 = [20, 1, 4, 6, 2, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, 18, 17, 22], parent2 = [14, 19, 6, 21, 8, 5, 10, 1, 4, 13, 12, 18, 7, 11, 20, 3, 15, 16, 2, 9, 17, 22]} {child1: [20, 8, 19, 6, 2, 21, 10, 1, 4, 13, 12, 18, 7, 11, 9, 15, 16, 14, 3, 5, 17, 22], child2: [14, 4, 6, 11, 1, 18, 8, 10, 19, 7, 9, 5, 12, 21, 20, 3, 15, 16, 2, 13, 17, 22]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=6, end=14); Step 2: Create offspring by exchanging the selected range: (child1=[20, 1, 4, 6, 2, 11, 10, 1, 4, 13, 12, 18, 7, 11, 13, 15, 16, 14, 3, 18, 17, 22], child2=[14, 19, 6, 21, 8, 5, 8, 10, 19, 7, 9, 5, 12, 21, 20, 3, 15, 16, 2, 9, 17, 22]); Step 3: Determine the mapping relationship to legalize offspring: (mapping1={10: 8, 1: 10, 4: 19, 13: 7, 12: 9, 18: 5, 7: 12, 11: 21}, mapping2={8: 10, 10: 1, 19: 4, 7: 13, 9: 12, 5: 18, 12: 7, 21: 11}); Step 4: Legalize children with the mapping relationsip and receive 2 result offsprings as shown.}\n'

in_context += 'Now, there are Python code and some examples of the second Crossover operator. The examples consist of 2 parent traces and 2 new generated traces with explanations:\n'
in_context += 'import random \n def second_operator(parent1, parent2): \n size = len(parent1) \n #Step 1: Select random crossover range in both 2 parents, avoid the first and last gene \n start, end = sorted(random.sample(range(1, size-2), 2)) \n # Step 2: Create proto-child by inheriting the selected range from its parent \n child1 = [None]*len(parent1) \n child1[start:end] = parent1[start:end] \n child2 = [None]*len(parent2) \n child2[start:end] = parent2[start:end] \n #Step 3: Fill in remaining positions in child1 with other cities in parent2 \n for i in range(len(parent2)):\n if parent2[i] not in child1:\n child1[child1.index(None)] = parent2[i] \n #Step 4: Fill in remaining positions in child2 with other cities in parent1: \n for i in range(len(parent1)):\n if parent1[i] not in child2:\n child2[child2.index(None)] = parent1[i] \n return child1, child2 \n'
in_context += '{parent1 = [20, 1, 4, 6, 2, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, 18, 17, 22], parent2 = [6, 8, 20, 1, 19, 21, 10, 11, 7, 12, 5, 9, 4, 3, 15, 16, 2, 14, 13, 18, 17, 22]} {child1: [6, 20, 1, 11, 4, 2, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, 18, 17, 22], child2: [20, 1, 6, 8, 19, 21, 10, 11, 7, 12, 5, 9, 4, 3, 15, 16, 2, 14, 13, 18, 17, 22]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=6, end=19); Step 2: Create proto-child by inheriting the selected range from its parent: (child1=[None, None, None, None, None, None, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, None, None, None], child2=[None, None, None, None, None, None, 10, 11, 7, 12, 5, 9, 4, 3, 15, 16, 2, 14, 13, None, None, None]); Step 3: Fill in remaining positions in child1 with other cities in parent2: child1=[6, 20, 1, 11, 4, 2, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, 18, 17, 22]; Step 4: Fill in remaining positions in child2 with other cities in parent1: child2=[20, 1, 6, 8, 19, 21, 10, 11, 7, 12, 5, 9, 4, 3, 15, 16, 2, 14, 13, 18, 17, 22]}\n'
in_context += '{parent1 = [16, 22, 15, 13, 14, 19, 6, 21, 8, 5, 10, 1, 4, 3, 12, 18, 7, 11, 20, 9, 17, 2], parent2 = [3, 12, 21, 8, 10, 19, 7, 11, 20, 1, 4, 6, 2, 14, 13, 16, 22, 15, 17, 18, 5, 9]} {child1: [21, 19, 6, 2, 14, 13, 16, 22, 8, 5, 10, 1, 4, 3, 12, 18, 7, 11, 20, 15, 17, 9], child2: [19, 21, 8, 5, 10, 3, 12, 18, 20, 1, 4, 6, 2, 14, 13, 16, 22, 15, 17, 7, 11, 9]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=8, end=19); Step 2: Create proto-child by inheriting the selected range from its parent: (child1=[None, None, None, None, None, None, None, None, 8, 5, 10, 1, 4, 3, 12, 18, 7, 11, 20, None, None, None], child2=[None, None, None, None, None, None, None, None, 20, 1, 4, 6, 2, 14, 13, 16, 22, 15, 17, None, None, None]); Step 3: Fill in remaining positions in child1 with other cities in parent2: child1=[21, 19, 6, 2, 14, 13, 16, 22, 8, 5, 10, 1, 4, 3, 12, 18, 7, 11, 20, 15, 17, 9]; Step 4: Fill in remaining positions in child2 with other cities in parent1: child2=[19, 21, 8, 5, 10, 3, 12, 18, 20, 1, 4, 6, 2, 14, 13, 16, 22, 15, 17, 7, 11, 9]}\n'
in_context += '{parent1 = [16, 22, 15, 13, 14, 19, 6, 21, 8, 5, 10, 1, 4, 3, 12, 18, 7, 11, 20, 9, 17, 2], parent2 = [1, 4, 6, 2, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 3, 18, 17, 22, 20]} {child1: [2, 11, 15, 13, 14, 19, 6, 21, 8, 5, 10, 1, 4, 3, 12, 18, 7, 9, 16, 17, 22, 20], child2: [22, 1, 6, 2, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 4, 3, 18, 20, 17]} Explanation: {Step 1: Select random crossover range in both 2 parents: (start=2, end=17); Step 2: Create proto-child by inheriting the selected range from its parent: (child1=[None, None, 15, 13, 14, 19, 6, 21, 8, 5, 10, 1, 4, 3, 12, 18, 7, None, None, None, None, None], child2=[None, None, 6, 2, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, None, None, None, None, None]); Step 3: Fill in remaining positions in child1 with other cities in parent2: child1=[2, 11, 15, 13, 14, 19, 6, 21, 8, 5, 10, 1, 4, 3, 12, 18, 7, 9, 16, 17, 22, 20]; Step 4: Fill in remaining positions in child2 with other cities in parent1: child2=[22, 1, 6, 2, 11, 8, 10, 19, 7, 9, 5, 12, 21, 13, 15, 16, 14, 4, 3, 18, 20, 17]}\n'

crx_task = 'Please follow the instruction step-by-step to generate 2 new offsprings:\n'
crx_task += '1. Now, you are given 2 parent solution traces: '
crx_task2 = '2. You can use ONE of the 2 mentioned Crossover Operators with the two traces in Step 1 to generate 2 new Offspring traces.'
crx_task2 += 'Directly give me 2 Offspring traces, bracketed the first Offspring with <Off1> and </Off1> and bracketed the second one with <Off2> and </Off2>. Not any explanation needed.'


# %%
mut_description = 'You are given a list of points with coordinates: {' + list2str() + '}. A solution is a trace, with the shortest possible length, that traveles each point exactly once.\n'
mut_description += 'You now be given 1 solution traces, your task is to do Mutation it and give me the result.\n'

m_context = 'Now, there are Python code and some examples of the first Mutation operator. The examples consist of origin trace and the new generated trace with explanations:\n'
m_context += 'import random \n def first_operator(origin_trace): \n size = len(origin_trace) \n #Step 1: Randomly select 2 positions in the original trace \n position1, position2 = random.sample(range(1, size - 2), 2) \n # Step 2: Swap 2 genes in the positions selected aboved \n origin_trace[position1], origin_trace[position2] = origin_trace[position2], origin_trace[position1] \n'
m_context += '{origin_trace = [10, 14, 9, 8, 1, 6, 5, 11, 3, 12, 7, 13, 4, 2]}; {mutated_trace = [10, 14, 11, 8, 1, 6, 5, 9, 3, 12, 7, 13, 4, 2]} Explanation: {Step 1: Randomly select 2 positions in the original trace: (position1 = 2, position2 = 7); Step 2: Swap 2 genes in the positions selected aboved to get the mutated_trace = [10, 14, 11, 8, 1, 6, 5, 9, 3, 12, 7, 13, 4, 2]}\n'
m_context += '{origin_trace = [3, 2, 10, 7, 6, 11, 14, 1, 9, 13, 12, 5, 8, 4]}; {mutated_trace = [3, 9, 10, 7, 6, 11, 14, 1, 2, 13, 12, 5, 8, 4]} Explanation: {Step 1: Randomly select 2 positions in the original trace: (position1 = 8, position2 = 1); Step 2: Swap 2 genes in the positions selected aboved to get the mutated_trace = [3, 9, 10, 7, 6, 11, 14, 1, 2, 13, 12, 5, 8, 4]}\n'
m_context += '{origin_trace = [8, 7, 12, 14, 1, 3, 11, 6, 10, 4, 9, 13, 5, 2]}; {mutated_trace = [8, 7, 12, 14, 1, 3, 10, 6, 11, 4, 9, 13, 5, 2]} Explanation: {Step 1: Randomly select 2 positions in the original trace: (position1 = 6, position2 = 8); Step 2: Swap 2 genes in the positions selected aboved to get the mutated_trace = [8, 7, 12, 14, 1, 3, 10, 6, 11, 4, 9, 13, 5, 2]}\n'

m_context += 'Now, there are Python code and some examples of the second Mutation operator. The examples consist of origin trace and the new generated trace with explanations:\n'
m_context += 'import random \n def second_operator(origin_trace): \n size = len(origin_trace) \n #Step 1: Select a random point in the original trace \n point = random.randint(0, size - 1) \n # Step 2: Reverse all the sub-sequences from 0 to point and from point + 1 to the end \n     mutated_trace = origin_trace[:point][::-1] + origin_trace[point:][::-1] \n return mutated_trace \n'
m_context += '{origin_trace = [4, 1, 5, 14, 3, 9, 11, 7, 12, 13, 2, 8, 6, 10]}; {mutated_trace = [5, 1, 4, 10, 6, 8, 2, 13, 12, 7, 11, 9, 3, 14]} Explanation: {Step 1: Select a random point in the original trace: (point = 3); Step 2: Reverse all the sub-sequences from index = 0 to 3  and from index = 4 to the end of origin_trace, and get mutated_trace = [5, 1, 4, 10, 6, 8, 2, 13, 12, 7, 11, 9, 3, 14]}\n'
m_context += '{origin_trace = [10, 7, 5, 4, 9, 12, 3, 6, 14, 8, 1, 11, 13, 2]}; {mutated_trace = [14, 6, 3, 12, 9, 4, 5, 7, 10, 2, 13, 11, 1, 8]} Explanation: {Step 1: Select a random point in the original trace: (point = 9); Step 2: Reverse all the sub-sequences from index = 0 to 9  and from index = 10 to the end of origin_trace, and get mutated_trace = [14, 6, 3, 12, 9, 4, 5, 7, 10, 2, 13, 11, 1, 8]}\n'
m_context += '{origin_trace = [4, 6, 14, 9, 8, 10, 7, 13, 2, 1, 5, 3, 12, 11]}; {mutated_trace = [12, 3, 5, 1, 2, 13, 7, 10, 8, 9, 14, 6, 4, 11]} Explanation: {Step 1: Select a random point in the original trace: (point = 13); Step 2: Reverse all the sub-sequences from index = 0 to 13  and from index = 14 to the end of origin_trace, and get mutated_trace = [12, 3, 5, 1, 2, 13, 7, 10, 8, 9, 14, 6, 4, 11]}\n'

m_context += 'Now, there are Python code and some examples of the third Mutation operator. The examples consists of origin trace and the new generated trace with explanations.\n'
m_context += 'import random \n def third_operator(origin_trace): \n size = len(origin_trace) \n #Step 1: Select reverse range at random \n start, end = sorted(random.sample(range(1, size - 1), 2)) \n #Step 2: Reverse the sub-sequence from start to end to have the mutated trace \n     mutated_trace = origin_trace[:start] + origin_trace[start:end][::-1] + origin_trace[end:] \n return mutated_trace \n'
m_context += '{origin_trace = [1, 4, 13, 7, 10, 12, 6, 3, 8, 2, 11, 9, 5, 14]}; {mutated_trace = [1, 4, 13, 7, 10, 12, 8, 3, 6, 2, 11, 9, 5, 14]} Explanation: {Step 1: Select reverse range at random: (start = 6, end = 9); Step 2: Reverse the sub-sequence from index = 6 to 9 to have the mutated trace: [1, 4, 13, 7, 10, 12, 8, 3, 6, 2, 11, 9, 5, 14]}\n'
m_context += '{origin_trace = [2, 14, 4, 7, 10, 3, 8, 5, 1, 11, 12, 13, 6, 9]}; {mutated_trace = [2, 14, 4, 7, 10, 3, 8, 5, 1, 11, 12, 13, 6, 9]} Explanation: {Step 1: Select reverse range at random: (start = 6, end = 7); Step 2: Reverse the sub-sequence from index = 6 to 7 to have the mutated trace: [2, 14, 4, 7, 10, 3, 8, 5, 1, 11, 12, 13, 6, 9]}\n'
m_context += '{origin_trace = [14, 10, 5, 2, 13, 7, 12, 4, 8, 1, 3, 11, 6, 9]}; {mutated_trace = [14, 10, 5, 2, 13, 7, 1, 8, 4, 12, 3, 11, 6, 9]} Explanation: {Step 1: Select reverse range at random: (start = 6, end = 10); Step 2: Reverse the sub-sequence from index = 6 to 10 to have the mutated trace: [14, 10, 5, 2, 13, 7, 1, 8, 4, 12, 3, 11, 6, 9]}\n'

mut_task = 'Please follow the instruction step-by-step to generate 1 new mutated trace:\n'
mut_task += '1. Now, you are given a solution trace: '
mut_task2 = '2. You CAN use ONE of the 3 Mutation Operators aboved or combine them and generate NEW operator to mutate the given original trace in Step 1.'
mut_task2 += 'Directly give me the result, bracketed it with <mut> and </mut>. Not any explanation needed.'

# %%
best_cur = 99999999
best_now = 9999990

Pool = randomFirstN(n, N)

g = 1

# %%
while (g <= G and not check_stuck(best_cur, best_now, K=10)) :

    best_cur = Pool[N-1].length

    Pool_sharp = []

    for i in range(1, N+1) :
        
        par1, par2 = tournament_selection(Pool)

        print(f"{i}th pairs of parents in generation {g}:")

        print(f"parent_1: {par1}, parent_2: {par2}")

        if (random.random() < 0.7) :

            crosOv_prompt = crx_description + (trace_samples + pool2examples(Pool)) + in_context + crx_task + parent2str(par1, par2) + crx_task2

            start_time = time.time()

            response = model.generate_content(contents=crosOv_prompt)

            spent_time = time.time() - start_time

            print(f"spent_time for this request: {spent_time}")

            print(f"crossover of {i}th parents in generation {g}")
            child1, child2 = cut2Offsprings(response.text)
            #print(child1, child2)

            if checkPermu(child1, n):
                print("child1 accepted!")
                Pool_sharp.append(Individual(trace=traceStr2list(child1), length=objective_TSP(traceStr2list(child1))))
            if checkPermu(child2, n):
                print("child2 accepted!")
                Pool_sharp.append(Individual(trace=traceStr2list(child2), length=objective_TSP(traceStr2list(child2))))

            if (random.random() < 0.2) :

                for childStr in [child1, child2]:

                    mutate_prompt = mut_description + (trace_samples + pool2examples(Pool)) + m_context + (mut_task + childStr) + mut_task2

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

    print(f"END generation: {g}, best solution now is: {best_now}")
    
    print("#######################################################################################")
    
    g += 1


print(best_now)


