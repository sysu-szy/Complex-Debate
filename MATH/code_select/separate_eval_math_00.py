import json
import numpy as np
import re
import os
import pandas as pd


def extrat_answer(input_str):
    pattern = r"boxed{.+}"

    matches = re.findall(pattern, input_str)
    if matches:
        return matches[-1][6:-1]

    return None


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
        agents_answer.append(extrat_answer(agent[max_round]))

    mode_answer = mode(agents_answer)
    real_answer = extrat_answer(gt)

    try:
        is_correct = mode_answer == real_answer
    except:
        is_correct = False

    if is_correct:
        return 1
    else:
        return 0


if __name__ == "__main__":
    levels = ["level1", "level2", "level3", "level4", "level5"]
    models = ["gpt-4"]
    question_num = 100
    agent_num = 4
    round_num = 3
    test_num = 1

    for level in levels:
        for use_model in models:
            data_path = f"D:/01_Study/02_Debate/Selection/code/MATH/math_exp_data/separate/{use_model}_separate_{agent_num}_{round_num}_test{test_num}/{level}"
            eval_filename = f"D:/01_Study/02_Debate/Selection/code/MATH/math_exp_data/separate/acc/{use_model}_separate_{agent_num}_{round_num}_test{test_num}_acc"

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

