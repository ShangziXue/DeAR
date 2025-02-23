from tqdm import tqdm
import json
from stages import Decompose, Solve, Self_Check, Score, Extract, Update
from queue import Queue

EPSILON1 = 0.4
EPSILON2 = 0.6
MAX_DEPTH = 4
MAX_BRANCH = 3

class Node:
    def __init__(self, level, question, rationale="", score=1.0):
        self.level = level
        self.question = question
        self.rationale = rationale
        self.score = score

    def is_endnode(self):
        return not (self.question or self.rationale or self.score)

def reasoning_tree_solver(Q, Heuristics):
    root = Node(level=0, question=Q)
    N = Queue()
    N.put(root)
    node_memory = [root]  

    while not N.empty():
        nt = N.get()  
        if nt.level > MAX_DEPTH:
            break
        if nt.is_endnode():
            continue
        if nt.score <= EPSILON1:
            N.put(Node(level=nt.level + 1, question="", rationale="", score=0))
            continue
        # Decompose
        sub_questions = Decompose(nt.question, Heuristics)  
        if len(sub_questions) > MAX_BRANCH:
            sub_questions = sub_questions[:MAX_BRANCH]
        new_nodes = []
        for sub_q in sub_questions:
            new_node = Node(level=nt.level + 1, question=sub_q)
            N.put(new_node)
            new_nodes.append(new_node)
            node_memory.append(new_node)
        # Analyze
        for n_t1 in new_nodes:
            r1 = Solve(n_t1.question) 
            r2 = Self_Check(n_t1.question, r1) 
            n_t1.rationale = r2
            n_t1.score = Score(n_t1.question, r2) 
        # Rethink
        for n_t1 in new_nodes:
            if n_t1.score > EPSILON2:
                # Extract
                prev_nodes = Extract(n_t1.question, n_t1.rationale, node_memory)  
                for n_prev in prev_nodes:
                    # Update
                    r3 = Update(n_t1.question, n_t1.rationale, n_prev.question, n_prev.rationale)
                    n_prev.rationale = r3 
    return root.rationale

if __name__ == "__main__":
    with open(f'../data/strategyqa/strategyqa_test_with_heuristics.json', 'r', encoding='utf-8') as f:
        test = json.load(f)
    results = []
    for item in tqdm(test):
        new_dict ={}
        new_dict["id"] = item["qid"]
        new_dict["question"] = item["question"]
        heuristics = item["heuristics"]
        examples_text = f"Decomposition Examples (logic heuristics):\n"
        for idx, example in enumerate(heuristics, 1):
            example_question = example[f"Example question {idx}: "]
            decomposition_list = example["Decomposition: "]
            examples_text += f"  Example {idx}: {example_question}\n  Decomposition: \n"
            for subq in decomposition_list:
                examples_text += ("subqestion:" + subq + ' ')
        new_dict["heuristics"] = examples_text
        new_dict["DeAR_rationale"] = reasoning_tree_solver(item["question"], examples_text)
        results.append(new_dict)
    with open('../data/strategyqa/strategyqa_test_output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)