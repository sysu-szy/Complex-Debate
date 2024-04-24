import json
import numpy as np
import re
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
    use_model = "gpt-3.5-turbo"
    question_num = 100
    agent_num = 4
    round_num = 3
    test_num = 1

    response_dict = json.load(open(
        f"D:\\01_Study\\02_Debate\\Selection\\code\\GSM8K\\gsm_exp_data\\select\\{use_model}_select_gsm_{question_num}_{round_num}_{agent_num}_test{test_num}.json",
        "r"))
    eval_filename = f"D:\\01_Study\\02_Debate\\Selection\\code\\GSM8K\\gsm_exp_data\\select\\{use_model}_select_gsm_{question_num}_{round_num}_{agent_num}_test{test_num}_acc"

    questions = list(response_dict.keys())
    accuracies = []

    for question in questions:
        i, agents_response, gt = response_dict[question]

        accurate = compute_accuracy(agents_response, gt)

        if accurate is not None:
            accuracies.append(float(accurate))
        else:
            import pdb

            pdb.set_trace()
            print(gt)

        print("accuracies:", np.mean(accuracies), np.std(accuracies) / (len(accuracies) ** 0.5))

    df = pd.DataFrame(accuracies, columns=['acc'])
    df.to_csv(f"{eval_filename}.csv")
