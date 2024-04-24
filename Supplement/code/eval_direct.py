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
    question_num = 100

    data_path = f"D:/01_Study/02_Debate/Selection/code/Supplement/exp_data/simple_cot"
    eval_filename = f"D:/01_Study/02_Debate/Selection/code/Supplement/exp_data/simple_cot_acc.csv"

    accuracies = []
    for i in range(question_num):
        if not os.path.exists(f"{data_path}/Question_{i}.json"):
            continue
        per_data = json.load(open(f"{data_path}/Question_{i}.json"))
        accurate = compute_accuracy(per_data["agents_response"], per_data["answer"])
        accuracies.append(accurate)
    print("accuracies:", np.mean(accuracies), "cnt:", len(accuracies))

    df = pd.DataFrame(accuracies, columns=['acc'])
    df.to_csv(f"{eval_filename}")