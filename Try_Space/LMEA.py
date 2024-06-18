import time

from support import *
from edAdj_instance import *

from instance import *


import google.generativeai as genai


genai.configure(api_key='_YOUR_API_KEY_',)

model = genai.GenerativeModel(model_name='gemini-pro')

#config = genai.GenerationConfig(temperature=1.5)

count_api_calls = 0


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


addition_promt = 'You have not give me enough ' + str(N) + ' traces. Please continue the mentioned instruction to generate more.'
#------------------------------------------------------------------------------------------------------------------------------------

Pool = randomFirstN(n, N)

g = 1

while g <= G :

    chat = model.start_chat(history=[])

    generation_startTime = time.time()

    prompt = description + (in_context + pool2examples(Pool)) + task_instruction

    listOff = []

    time_callGen = time.time()

    response = chat.send_message(prompt)

    count_api_calls += 1

    cost_forMainCall = time.time() - time_callGen

    print(f"time cost for {count_api_calls}th call in the generation {g}: {cost_forMainCall: .2f}")

    try:
        newGen = cutGenTrace(response.text)
    except:
        response = chat.send_message(prompt)
        count_api_calls += 1

    for s in newGen:
        if checkPermu(s, n) :
                listOff.append(s)
    
    count_additionCall = 0

    while len(listOff) < N:
        time_callAdd = time.time()

        if count_additionCall < 4:
            addition = chat.send_message(addition_promt)
            count_additionCall += 1
        else :
            addition = chat.send_message(prompt)
            count_additionCall = 0

        count_api_calls += 1

        cost_forAddCall = time.time() - time_callAdd

        print(f"time cost for {count_api_calls}th call in the generation {g}: {cost_forAddCall: .2f}")

        try:
             newAdd = cutGenTrace(addition.text)
        except:
             addition = chat.send_message(prompt)
             count_api_calls += 1
        
        for ss in newAdd:
             if checkPermu(ss, n):
                  listOff.append(ss)
    
    P_sharp = transform(listOff[:N])

    Pool = updatePool(Pool, P_sharp, N)

    generation_time = time.time() - generation_startTime

    print(f"generation {g} time cost: {generation_time: .2f}")

    g += 1

print(Pool[N-1])



#---------------------------------------------------------------------------------------------------------------------------------------
'''
while len(listOff) < N :

        call_startTime = time.time()

        count_api_calls += 1

        response = chat.send_message(prompt)

        call_time = time.time() - call_startTime

        print(f"time cost for {count_api_calls}th call in the generation {g}: {call_time: .2f}")

        try:
            newGen = cutGenTrace(response.text)
        except:
            continue
        for s in newGen:
            if checkPermu(s, n) :
                listOff.append(s)
'''

#-----------------------------------------------------------------------------------------------------------------------------------
# Test space:
'''
prompt = description + (in_context + pool2examples(Pool)) + task_instruction

listOff = []
while len(listOff) < N :
    response = chat.send_message(prompt)
    newGen = cutGenTrace(response.text)
    for s in newGen:
        listOff.append(s)
P_sharp = transform(listOff[:N])

print(P_sharp)

Pool = updatePool(Pool, P_sharp, N)


print(Pool)
'''