import os
import json
import time
import random
import openai
from openai import OpenAI


def generate_answer(use_model, context):
    client = OpenAI()
    completion = client.chat.completions.create(
        model=use_model,
        messages=context,
    )
    content = completion.choices[0].message.content
    time.sleep(2)
    return content


if __name__ == "__main__":
    use_model = "gpt-4"
    question_num = 100
    method = "simple_cot"

    root_path = "D:/01_Study/02_Debate/Selection/code/Supplement"
    row_data = json.load(open(f"{root_path}/row_data/math_level5_random_100.json"))

    output_path = f"{root_path}/exp_data"
    if not os.path.exists(f"{output_path}/{method}"):
        os.makedirs(f"{output_path}/{method}")
    output_path = f"{output_path}/{method}"

    error_response_num = []

    for i in range(question_num):
        is_error_continue = False
        print('\n', f"Question {i}")
        response_dict = {}

        save_name = f"{output_path}/Question_{i}.json"
        if os.path.exists(save_name):
            continue

        question, answer = row_data[str(i)]
        response_dict["question"] = question
        response_dict["answer"] = answer
        agent_prompt = [{"role": "user",
                         "content": """Given a mathematics problem, determine the answer. \nQuestion: {}\nExamine your solution step by step. Simplify your answer as much as possible. Your final answer should be in the form \\boxed{{answer}}, at the end of your response.""".format(
                             question)}]

        try:
            agent_answer = generate_answer(use_model, agent_prompt)
        except openai.BadRequestError as e:
            error_response_num.append(i)
            json.dump(error_response_num, open(f"{output_path}/error_response_num.json", "w"))
            is_error_continue = True
            continue

        response_dict["agents_response"] = agent_answer
        json.dump(response_dict, open(f"{save_name}", "w"))

