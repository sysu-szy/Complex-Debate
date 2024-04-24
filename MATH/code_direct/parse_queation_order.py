import json
import numpy as np
import re
import os
import pandas as pd


def extrat_answer(input_str):
    pattern = r"boxed{[0-9.]+}"
    matches = re.findall(pattern, input_str)
    if matches:
        return int(eval(matches[-1][6:-1]))
    return None


def get_answer(input_str):
    pattern = r"#### [0-9.]+"

    matches = re.findall(pattern, input_str)
    if matches:
        return int(matches[-1][5:])

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
    real_answer = get_answer(gt)

    try:
        is_correct = mode_answer == real_answer
    except:
        is_correct = False

    if is_correct:
        return 1
    else:
        return 0


if __name__ == "__main__":
    use_models = ["gpt-3.5-turbo", "gpt-4"]
    levels = ["level1", "level2", "level3", "level4", "level5"]
    question_num = 100
    agent_num = 4
    round_num = 3
    test_num = 1

    root_path = "D:/01_Study/02_Debate/Selection/code/MATH"

    for level in levels:
        for use_model in use_models:
            row_data = json.load(open(f"{root_path}/math_row_data/random_questions/{level}/math_random_100.json"))

            agent_data = json.load(open(f"{root_path}/math_exp_data/direct/{level}/response/{use_model}_direct_math_100.json"))
            agent_questions = list(agent_data.keys())

            accuracies = []
            cnt = 0
            for i in range(question_num):
                question = row_data[str(i)][0]
                answer = row_data[str(i)][1]
                if question in agent_questions:
                    cnt += 1
            print(cnt)


