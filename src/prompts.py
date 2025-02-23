PROMPT_TEMPLATES = {
    #Decompose
    "Decompose_head": ''' Your task is to decompose the given question Q into sub-questions. You should based on the specific logic of the question to determine the number of sub-questions and output them sequentially. If you consider the question Q to be sufficiently simple and no further decomposition is needed, then output “End.” I will provide you with three questions similar to q, along with their decomposed sub-questions as examples. You can learn from these examples on how to decompose such questions, and then apply what you’ve learned to decompose Q.\n
    ''',
    "Decompose_instruction": ''' Please note that: If Q can be decomposed, you should output multiple sub-questions as shown in the above Logic Heuristics. Otherwise please output “End”. The decomposed sub-questions for Q is:\n
    ''',
    #Analyze
    "Solve_head": '''Answer the following question and provide a detailed reasoning process.\n''',
    "Solve_instruction": '''Your reasoning process:\n''',

    "Self_Check_head": '''There might be some errors in the rationale for the following question. If you believe there are errors, please correct them and provide the accurate reasoning process. Otherwise, output the original reasoning process.\n''',
    "Self_Check_instruction": '''Your output:\n''',

    "Score_head": '''Please rate the overall correctness and logic of the following rationale on a scale from 1 to 10, where 1 is the lowest score and 10 is the highest score. Divide the chosen integer by 10 and output it as the final score.\n''',
    "Score_instruction": '''Your score:\n''',
    #Rethink
    "Extract_head": '''Please extract questions from the following list that might use the answer of q to update their rationales. Question list:\n''',
    "Extract_instruction": '''Your extracted questions:\n''',

    "Update_head": '''Please update the answer to question b based on the answer to question a.\n''',
    "Update_instruction": '''The updated answer to question b is:\n''',
}

def get_prompt(template_name):
    template = PROMPT_TEMPLATES.get(template_name)
    if not template:
        raise ValueError(f"Prompt template '{template_name}' not found.")
    return template
