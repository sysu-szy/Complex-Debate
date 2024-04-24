import json
import numpy as np
import re
import pandas as pd
import os

def parse_answer(input_str):
    pattern = r'\((\w)\)'
    matches = re.findall(pattern, input_str)

    solution = None

    for match_str in matches[::-1]:
        solution = match_str.upper()
        if solution:
            break

    return solution

def compute_accuracy(responses, gt):
    if gt == parse_answer(responses):
        return 1
    else:
        return 0


if __name__ == "__main__":
    use_models = ["gpt-3.5-turbo", "gpt-4"]
    question_num = 100
    test_num = 1

    for use_model in use_models:
        data_path = f"D:/01_Study/02_Debate/Selection/code/MMLU/mmlu_exp_data/direct/{use_model}_response"
        eval_filename = f"D:/01_Study/02_Debate/Selection/code/MMLU/mmlu_exp_data/direct/{use_model}_direct_mmlu_{question_num}_acc"

        accuracies = []
        for i in range(question_num):
            if not os.path.exists(f"{data_path}/Question_{i}.json"):
                continue
            per_data = json.load(open(f"{data_path}/Question_{i}.json"))
            accurate = compute_accuracy(per_data["agents_response"], per_data["answer"])
            accuracies.append(accurate)
        print("accuracies:", np.mean(accuracies), "cnt:", len(accuracies))

        df = pd.DataFrame(accuracies, columns=['acc'])
        df.to_csv(f"{eval_filename}.csv")
