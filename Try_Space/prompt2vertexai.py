import time

from support import *
from edAdj_instance import *

from instance import *


import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# TODO(developer): Update and un-comment below line
project_id = "_YOUR_PRJ_ID_"

vertexai.init(project=project_id, location="us-central1")

model = GenerativeModel(model_name="gemini-1.5-pro-001")

count_api_calls = 0
#----------------------------------------------------------------------------------------------------------------------------------
description = 'You are given a list of points with coordinates: {' + list2str() + '}. Your task is to find a trace, with the shortest possible length, that traveles each point exactly once.\n'

in_context = 'Below are some previous traces and their lengths. The traces are arranged in descending order based on their lengths, where lower values are better.\n'
#in_context += pool2examples(Pool)                  ! NOTICE that each generation, Pool change.

task_instruction = 'Please follow the instruction step-by-step to generate new trace:\n'
task_instruction += 'Step 1. Select two traces from the above traces.\n'
task_instruction += 'Step 2. Crossover the two traces chosen in Step 1 and generate a new trace.\n'
task_instruction += 'Step 3. Mutate the trace generated in Step 2 and generate a new trace.\n'
task_instruction += ('Step 4. Keep the generated trace generated in Step 3, repeat Step 1, 2, 3, until you have ' + str(N) + ' generated traces.\n')
task_instruction += 'Directly give me all the chosen traces at Step 1, bracketed them with <selection> and </selection>, and all the generated traces at Step 3, bracketed them with <res> and </res>. Not any explanation needed.'


addition_promt = 'You have not give me enough ' + str(N) + ' traces. Please continue the mentioned instruction to generate more.'
#----------------------------------------------------------------------------------------------------------------------------------
Pool = randomFirstN(n, N)

g = 1

cur_temp = 1.0

while g <= G :

    best_cur = Pool[N-1].length

    config = GenerationConfig(temperature=cur_temp)

    start_gen = time.time()

    prompt = description + (in_context + pool2examples(Pool)) + task_instruction

    listOff = []
    while len(listOff) < N :

        start_call = time.time()

        response = model.generate_content(contents=prompt, generation_config=config)

        count_api_calls += 1

        spent_time = time.time() - start_call

        if spent_time < 30:
            time.sleep(30-spent_time)

        print(f"Time for {count_api_calls}th call in generation {g} is: {spent_time: .2f}")

        try:
            newGen = cutGenTrace(response.text)
        except:
            continue
        for s in newGen:
            if checkPermu(s, n) :
                listOff.append(s)
    P_sharp = transform(listOff[:N])

    Pool = updatePool(Pool, P_sharp, N)

    proc_time = time.time() - start_gen

    print(f"Total time for generation {g} is: {proc_time: .2f}")

    best_now = Pool[N-1].length

    if check_stuck(best_cur, best_now):
        print("***Seft adaption for LLM")
        cur_temp += 0.1

    g += 1

print(Pool[N-1])
