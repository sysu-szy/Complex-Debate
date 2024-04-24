import json
import numpy as np
import re
import os
import pandas as pd


def parse_answer(input_str):
    pattern = r'\((\w)\)'
    matches = re.findall(pattern, input_str)

    solution = None

    for match_str in matches[::-1]:
        solution = match_str.upper()
        if solution:
            break

    return solution


def mode(agents_answer):
    ans = max(set(agents_answer), key=agents_answer.count)
    if agents_answer.count(ans) == 1:
        return None
    return ans


def compute_accuracy(agents_response, gt):
    rounds = list(agents_response[0].keys())
    max_round = max(rounds)

    agents_answer = []
    for agent in agents_response:
        agents_answer.append(parse_answer(agent[max_round]))

    mode_answer = mode(agents_answer)

    try:
        is_correct = mode_answer == gt
    except:
        is_correct = False

    if is_correct:
        return 1
    else:
        return 0


if __name__ == "__main__":
    use_model = "gpt-3.5-turbo"
    question_num = 100
    agent_num = 4
    round_num = 3
    test_num = 1

    data_path = f"D:/01_Study/02_Debate/Selection/code/MMLU/mmlu_exp_data/separate/{use_model}_separate_{agent_num}_{round_num}_test{test_num}"
    eval_filename = f"D:/01_Study/02_Debate/Selection/code/MMLU/mmlu_exp_data/separate/{use_model}_separate_mmlu_{question_num}_{agent_num}_{round_num}_test{test_num}_acc"

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
