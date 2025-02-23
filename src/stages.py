import json
from backbone import chatgpt_inference, llama_inference, chatglm_inference
from prompts import get_prompt

MODEL_NAME = "chatgpt"

function_map = {
    "chatgpt": chatgpt_inference,
    "llama": llama_inference,
    "chatglm": chatglm_inference
}

def Decompose(question, heuristics):
    head = get_prompt("Decompose_head")
    instruction = get_prompt("Decompose_instruction")
    prompt = head + "Logic Heuristics:\n" + heuristics + \
    "The given question Q: " + question + "\n" + instruction + \
    "Please output the decomposed sub-questions as a string in list format, where each element represents the text of a sub-question, in the form of '[\"subq1\", \"subq2\", \"subq3\"]'."
    string_data = function_map[MODEL_NAME](prompt)
    try:
       list_data = json.loads(string_data)
    except (json.JSONDecodeError, TypeError) as e:
       list_data = [question]
    return list_data


def Solve(question):
    head = get_prompt("Solve_head")
    instruction = get_prompt("Solve_instruction")
    prompt = head + "Question: " + question + "\n" + instruction
    rationale = function_map[MODEL_NAME](prompt)
    return rationale

def Self_Check(question, result):
    head = get_prompt("Self_Check_head")
    instruction = get_prompt("Self_Check_instruction")
    prompt = head + "Question: " + question + "\n" + "Rationale: " + result + "\n" + instruction
    rationale = function_map[MODEL_NAME](prompt)
    return rationale

def Score(question, rationale):
    head = get_prompt("Score_head")
    instruction = get_prompt("Score_instruction")
    prompt = head + "Question: " + question + "\n" + "Rationale: " + rationale + "\n" + "Your should only output an integer. " + instruction
    score = int(function_map[MODEL_NAME](prompt))
    return score/10 

def Extract(question, rationale, node_memory):
    node_map = {}
    for node in node_memory:
        node_map[node.question] = node.rationale
    head = get_prompt("Extract_head")
    instruction = get_prompt("Extract_instruction")
    prompt = head + "Question list: \n"
    idx = 1
    for node in node_memory:
        prompt += (f"{idx}: " + node.question + "\n")
        idx += 1
    prompt += ("q: " + question + "\n" + "The answer of q: " + rationale + "\n")
    prompt += "Please output the indices of the extracted questions as a string in list format, where each element represents the index of a question, in the form of '[\"1\", \"2\", \"3\"]'."
    prompt += instruction
    string_question = function_map[MODEL_NAME](prompt)
    list_question = json.loads(string_question)
    memory_list = []
    for ids in list_question:
        memory_list.append(node_memory[ids-1])
    return memory_list

def Update(new_question, new_rationale, prev_question, prev_rationale):
    head = get_prompt("Update_head")
    instruction = get_prompt("Update_instruction")
    prompt = head + "Question a: " + new_question + "\n" + "The answer to question a: " + new_rationale + "\n" + "Question b: " + prev_question + "\n" + "The answer to question b: " + prev_rationale + "\n" + instruction
    return function_map[MODEL_NAME](prompt)

