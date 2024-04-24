from glob import glob
import pandas as pd
import json
import time
import os
import random
import openai
from openai import OpenAI

def generate_answer(use_model, context):
    client = OpenAI(api_key="")
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
    test_num = 1

    root_path = "D:/01_Study/02_Debate/Selection/code/MMLU"
    questions = json.load(open(f"{root_path}/mmlu_row_data/mmlu_random_100.json", "r"))
    output_path = f"{root_path}/mmlu_exp_data/direct/{use_model}_response"

    error_response_num = []
    for i in range(question_num):
        is_error_continue = False
        print('\n', f"Question {i}")
        generated_description = {}

        save_name = f"{output_path}/Question_{i}.json"
        if os.path.exists(save_name):
            continue

        question, answer = questions[str(i)]
        generated_description["question"] = question
        generated_description["answer"] = answer

        question = "Can you answer the following question as accurately as possible?" + question + "Explain your answer, putting the answer in the form (X) at the end of your response."
        agent_prompt = [{"role": "user", "content": question}]

        try:
            agent_answer = generate_answer(use_model, agent_prompt)
        except openai.BadRequestError as e:
            error_response_num.append(i)
            json.dump(error_response_num, open(f"{output_path}/error_response_num.json", "w"))
            is_error_continue = True
            continue

        generated_description["agents_response"] = agent_answer
        json.dump(generated_description, open(f"{save_name}", "w"))



