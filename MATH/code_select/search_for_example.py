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
    use_model = "gpt-4"
    question_num = 100
    agent_num = 4
    round_num = 3
    test_num = 1
    level = "level5"

    file_folder_name = "gpt-4_separate_4_3_test1"
    data_path = f"D:/01_Study/02_Debate/Selection/code/MATH/math_exp_data/separate/{file_folder_name}/{level}"

    accuracies = []
    for i in range(question_num):
        if not os.path.exists(f"{data_path}/Question_{i}.json"):
            continue
        per_data = json.load(open(f"{data_path}/Question_{i}.json"))
        accurate = compute_accuracy(per_data["agents_response"], per_data["answer"])

        if accurate:
            print("\nQuestion:", i)
            my_answers = []
            real_answer = extrat_answer(per_data["answer"])
            for j in range(round_num):
                for k in range(agent_num):
                    my_answers.append(extrat_answer(per_data["agents_response"][k][f"round {j}"]))
            print(my_answers)

