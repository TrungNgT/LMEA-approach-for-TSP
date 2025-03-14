from support import *
from instance import *


import google.generativeai as genai


genai.configure(api_key='Your_API_key')

model = genai.GenerativeModel(model_name='gemini-pro')

chat = model.start_chat(history=[])
#----------------------------------------------------------------------------------------------------------------------------------

description = 'You are given a list of points with coordinates: {' + list2str() + '}. Your task is to find a trace, with the shortest possible length, that trverses each point exactly once.\n'

in_context = 'Below are some previous traces and their lengths. The traces are arranged in descending order based on their lengths, where lower values are better.\n'
#in_context += pool2examples(Pool)                  ! NOTICE that each generation, Pool change.

task_instruction = 'Please follow the instruction step-by-step to generate new trace:\n'
task_instruction += 'Step 1. Select two traces from the above traces.\n'
task_instruction += 'Step 2. Crossover the two traces chosen in Step 1 and generate a new trace.\n'
task_instruction += 'Step 3. Mutate the trace generated in Step 2 and generate a new trace.\n'
task_instruction += ('Step 4. Keep the generated trace generated in Step 3, repeat Step 1, 2, 3, until you have ' + str(N) + ' generated traces.\n')
task_instruction += 'Directly give me all the chosen traces at Step 1, bracketed them with <selection> and </selection>, and all the generated traces at Step 3, bracketed them with <res> and </res>. Not any explanation needed.'

#------------------------------------------------------------------------------------------------------------------------------------

Pool = randomFirstN(n, N)

'''
while g <= G :

    prompt = description + (in_context + pool2examples(Pool)) + task_instruction

    listOff = []
    while len(listOff) < N :
        response = chat.send_message(prompt)
        newGen = cutGenTrace(response.text)
        for s in newGen:
            listOff.append(s)
        listOff.clear()
    P_sharp = transform(listOff[:N])

    tem = updatePool(Pool, P_sharp, N)
    Pool.clear()
    Pool = tem

'''

#-----------------------------------------------------------------------------------------------------------------------------------
# Test space:

prompt = description + (in_context + pool2examples(Pool)) + task_instruction

listOff = []
while len(listOff) < N :
    response = chat.send_message(prompt)
    newGen = cutGenTrace(response.text)
    for s in newGen:
        listOff.append(s)
    listOff.clear()
P_sharp = transform(listOff[:N])

print(P_sharp)

tem = updatePool(Pool, P_sharp, N)
Pool.clear()
Pool = tem

print(Pool)
