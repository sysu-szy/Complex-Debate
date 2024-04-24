import json
import numpy as np
import time
import re
import pandas as pd


def extrat_answer(input_str):
    pattern = r"boxed{.+}"

    matches = re.findall(pattern, input_str)
    if matches:
        return matches[-1][6:-1]

    return None


def compute_accuracy(gt, response):
    try:
        is_correct = extrat_answer(gt) == extrat_answer(response)
    except:
        is_correct = False

    if is_correct:
        return 1
    else:
        return 0


if __name__ == "__main__":
    use_model = "gpt-4"
    level = "level2"
    question_num = 100

    output_path = f"D:\\01_Study\\02_Debate\\Selection\\code\\MATH\\math_exp_data\\direct\\{level}"
    response_dict = json.load(open(f"{output_path}\\response\\{use_model}_direct_math_{question_num}.json"))
    eval_filename = f"{output_path}\\accurate\\acc_direct_math_{question_num}"

    questions = list(response_dict.keys())
    accuracies = []

    for question in questions:
        _, response, gt = response_dict[question]
        accurate = compute_accuracy(gt, response)

        if accurate is not None:
            accuracies.append(float(accurate))
        else:
            import pdb

            pdb.set_trace()
            print(gt)

        print("accuracies:", np.mean(accuracies), np.std(accuracies) / (len(accuracies) ** 0.5))

    df = pd.DataFrame(accuracies, columns=[f"{use_model}"])
    df.to_csv(f"{eval_filename}.csv", mode='a')
