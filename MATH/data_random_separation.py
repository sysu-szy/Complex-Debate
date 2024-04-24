import pandas as pd
import os
import shutil
import json
import random

"""
algebra
{'1': 135, '2': 201, '3': 261, '4': 283, '5': 307}
counting_and_probability
{'1': 39, '2': 101, '3': 100, '4': 111, '5': 123}
geometry
{'1': 38, '2': 82, '3': 102, '4': 125, '5': 132}
intermediate_algebra
{'1': 52, '2': 128, '3': 195, '4': 248, '5': 280}
number_theory
{'1': 30, '2': 92, '3': 122, '4': 142, '5': 154}
prealgebra
{'1': 86, '2': 177, '3': 224, '4': 191, '5': 193}
precalculus
{'1': 57, '2': 113, '3': 127, '4': 114, '5': 135}
"""

def print_level_cnt():
    data_path = "D:\\01_Study\\02_Debate\\Selection\\dataset\\MATH\\MATH\\test\\"
    subjects = os.listdir(data_path)

    for subject in subjects:
        print(subject)
        level_count = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
        questions_path = os.listdir(f"{data_path}\\{subject}")
        for question_path in questions_path:
            question_all = json.load(open(f"{data_path}\\{subject}\\{question_path}", encoding='utf-8'))
            level = question_all["level"][-1]
            if level in list(level_count.keys()):
                level_count[level] += 1
        print(level_count)

if __name__ == "__main__":
    data_path = "D:\\01_Study\\02_Debate\\Selection\\dataset\\MATH\\MATH\\test\\"
    copy_path = "D:\\01_Study\\02_Debate\\Selection\\code\\MATH\\math_row_data\\"
    subjects = os.listdir(data_path)

    for subject in subjects:
        if not os.path.exists(f"{copy_path}\\subject\\{subject}"):
            os.makedirs(f"{copy_path}\\subject\\{subject}")
        questions_path = os.listdir(f"{data_path}/{subject}")

        for question_path in questions_path:
            question_all = json.load(open(f"{data_path}/{subject}/{question_path}", encoding='utf-8'))
            level = question_all["level"][-1]

            if not os.path.exists(f"{copy_path}\\subject\\{subject}\\level{level}"):
                os.makedirs(f"{copy_path}\\subject\\{subject}\\level{level}")
            shutil.copy(f"{data_path}/{subject}/{question_path}",f"{copy_path}\\subject\\{subject}\\level{level}")

            if not os.path.exists(f"{copy_path}\\level\\level{level}"):
                os.makedirs(f"{copy_path}\\level\\level{level}")
            shutil.copy(f"{data_path}/{subject}/{question_path}", f"{copy_path}\\level\\level{level}\\{subject}_{question_path}")

