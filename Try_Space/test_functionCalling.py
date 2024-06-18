import time

from support import *
from edAdj_instance import *

from instance import *


import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, FunctionDeclaration, Part, Tool

# TODO(developer): Update and un-comment below line
project_id = "_YOUR_PRJ_ID_"

vertexai.init(project=project_id, location="us-central1")



prompt = "You are given the sentence: 'Good Morning, how can I help you ?'. Your task is to use that sentence as the input parameter in my_custom_function and give me the result."

#----------------------------------------------------------------------------------

function_name = "my_custom_function"

custom_func = FunctionDeclaration(
    name = function_name,
    description = "You are given a sentence S. Your task is to remove all the space character in it.",

    parameters={
        "type": "object",
        "properties": {"S": {"type": "string"},},
    }

)

cal_tool = Tool(
    function_declarations=[custom_func]
)

model = GenerativeModel(model_name="gemini-1.5-pro-001", tools=[cal_tool])

response = model.generate_content(contents=prompt)

print(response.text)