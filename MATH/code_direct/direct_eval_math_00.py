import json
import numpy as np
import re
import pandas as pd
import os


def extrat_answer(input_str):
    pattern = r"boxed{.+}"

    matches = re.findall(pattern, input_str)
    if matches:
        return matches[-1][6:-1]

    return None


def compute_accuracy(response, gt):
    try:
        is_correct = extrat_answer(gt) == extrat_answer(response)
    except:
        is_correct = False

    if is_correct:
        return 1
    else:
        return 0


if __name__ == "__main__":
    levels = ["level1", "level2", "level3", "level4", "level5"]
    models = ["gpt-3.5-turbo", "gpt-4"]
    question_num = 100

    for level in levels:
        for use_model in models:
            data_path = f"D:/01_Study/02_Debate/Selection/code/MATH/math_exp_data/direct/{level}/{use_model}_separate"
            eval_filename = f"D:/01_Study/02_Debate/Selection/code/MATH/math_exp_data/direct/{level}/{use_model}_separate_math_{question_num}_acc"

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


