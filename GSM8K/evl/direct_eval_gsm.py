import json
import numpy as np
import re
import pandas as pd

def extrat_answer(input_str):
    pattern = r"boxed{.+}"

    matches = re.findall(pattern, input_str)
    if matches:
        return matches[-1][6:-1]

    return None



def get_answer(input_str):
    pattern = r"#### [0-9.]+"

    matches = re.findall(pattern, input_str)
    if matches:
        return matches[-1][5:]

    return None


def compute_accuracy(response, gt):
    try:
        is_correct = extrat_answer(response) == get_answer(gt)
    except:
        is_correct = False

    if is_correct:
        return 1
    else:
        return 0

if __name__ == "__main__":
    use_model = "gpt-4"
    question_num = 5
    test_num = 1

    response_dict = json.load(open(f"D:\\01_Study\\02_Debate\\Selection\\code\\GSM8K\\gsm_exp_data\\direct\\{use_model}_direct_gsm_{question_num}_test{test_num}.json", "r"))
    eval_filename = f"D:\\01_Study\\02_Debate\\Selection\\code\\GSM8K\\gsm_exp_data\\direct\\{use_model}_direct_gsm_{question_num}_test{test_num}_acc"

    questions = list(response_dict.keys())
    accuracies = []

    for question in questions:
        i, response, gt = response_dict[question]

        accurate = compute_accuracy(response, gt)

        if accurate is not None:
            accuracies.append(float(accurate))
        else:
            import pdb
            pdb.set_trace()
            print(gt)

        print("accuracies:", np.mean(accuracies), np.std(accuracies) / (len(accuracies) ** 0.5))

    df = pd.DataFrame(accuracies, columns=['acc'])
    df.to_csv(f"{eval_filename}.csv")