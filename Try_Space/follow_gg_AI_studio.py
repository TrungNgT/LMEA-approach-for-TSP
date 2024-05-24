from support import *

import google.generativeai as genai


genai.configure(api_key='Your_API_key')

def finding_0(X) :
    for x in str(X) :
        if x == '0':
            return True
    
    return False

model = genai.GenerativeModel(model_name='gemini-pro')
#response = model.generate_content('Which are popular crossover and mutation operators for solving TSP with EA?')

#print(response.text)
N = 3
G = 10

description = 'You are given number from 1 to 7. Your task is to generate a permutation that has best evaluation, following the Rule: the 2nd, 4th and 5th number must be even number. The Evaluation function of a permutation is the sum of first 4 numbers of it. '
in_context = 'Below are ' + str(N) +' example permutations and their evaluation. The list is arranged in descending order based on their evaluation, where lower are better: {{1, 4, 5, 6, 2, 3, 7} evaluation = 1+4+5+6 = 16}; {{5, 4, 3, 2, 6, 7, 1} evaluation = 5+4+3+2=14}; {{3, 2, 1, 4, 6, 7, 5} evaluation = 3+2+1+4=10}. '
task_instruction = 'Please follow the instruction step-by-step to show result: 1. Generate ' + str(N) +' permutations with the mentioned Rule above. 2. Evaluate each permutation by the described Evaluation function above. Directly give me each permutation, bracketed it with <per> and </per>, and its evaluation value bracketed with <eva> </eva> in one line. Not any explaination needed.'

# The prompt say result will be given bracketed in pair of tags so we can detect demanded value as number.

g = 1

while(g <= G) :
    prompt = description + in_context + task_instruction
    response = model.generate_content(prompt)
    print(response.text)
    g += 1

'''

prompt1 = 'Generate a function name trung(), the input parameter is an integer x, output of the function is (10*x). '
prompt2 = 'Randomly generate an integer in range [100, 200], called i. Directly give me the result of trung(i). No explanations are needed.'

chat = model.start_chat(history=[])

'''
'''
responce = chat.send_message(prompt1)
print(responce.text)

for k in range (6) :
    result = chat.send_message(prompt2)

print(result.text)



prompt3 = 'Randomly generate a number between 1 and 1001. Use the function finding_0() to return the result of the generated number.'

result = chat.send_message(prompt3)

print(result.text)
#print(genai.count_text_tokens(model, prompt='Please summarise this document: "1+1+1=3 but 1+1 is 2" in only one sentence. Write the sentence inside sections <res> </res>')) 
'''
