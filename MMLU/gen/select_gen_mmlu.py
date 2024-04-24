from glob import glob
import pandas as pd
import json
import time
import random
import openai
from openai import OpenAI
import os

ROLE_MMLU = ["You are a super-intelligent AI assistant capable of performing tasks more effectively than humans.",
             "You are a mathematician. You are good at math games, arithmetic calculation, and long-term planning.",
             "You are an economist. You are good at economics, finance, and business. You have experience on understanding charts while interpreting the macroeconomic environment prevailing across world economies.",
             "You are a psychologist. You are good at psychology, sociology, and philosophy. You give people scientific suggestions that will make them feel better.",
             "You are a lawyer. You are good at law, politics, and history.",
             "You are a doctor and come up with creative treatments for illnesses or diseases. You are able to recommend conventional medicines, herbal remedies and other natural alternatives. You also consider the patient’s age, lifestyle and medical history when providing your recommendations.",
             "You are a programmer. You are good at computer science, engineering, and physics. You have experience in designing and developing computer software and hardware.",
             "You are a historian. You research and analyze cultural, economic, political, and social events in the past, collect data from primary sources and use it to develop theories about what happened during various periods of history."]


def parse_question_answer(df, ix):
    question = df.iloc[ix, 0]
    a = df.iloc[ix, 1]
    b = df.iloc[ix, 2]
    c = df.iloc[ix, 3]
    d = df.iloc[ix, 4]

    question = "{}: A) {}, B) {}, C) {}, D) {}".format(question, a, b, c, d)

    answer = df.iloc[ix, 5]

    return question, answer


def save_random_question(question_num):
    tasks = glob("D:\\01_Study\\02_Debate\\Selection\\dataset\\MMLU\\test\\*.csv")
    dfs = [pd.read_csv(task) for task in tasks]
    output_path = f"D:/01_Study/02_Debate/Selection/code/MMLU/mmlu_row_data/mmlu_random_{question_num}"

    random.seed(0)
    random_questions = {}
    for i in range(question_num):
        len_dfs = len(dfs)
        idfs = random.randint(0, len_dfs - 1)
        df = dfs[idfs]
        ix = len(df)
        idx = random.randint(0, ix - 1)
        question, answer = parse_question_answer(df, idx)
        random_questions[str(i)] = (question, answer)

    json.dump(random_questions, open(f"{output_path}.json", "w"))


def construct_message(agents_response, question, round, agent):
    refer_response = agents_response[0:agent] + agents_response[agent + 1:]
    self_response = agents_response[agent]

    if round == 0:
        prefix_string = random.choice(ROLE_MMLU) + "\nIt's a debate to the following problem.\n" + question + "Explain your answer, putting the answer in the form (X) at the end of your response."
        return [{"role": "user",
                "content": prefix_string}]

    prefix_string = random.choice(ROLE_MMLU) + "\nIt's a debate to the following problem.\n" + question

    prefix_string = prefix_string + "\n\nIt's your solution from the last round:\n" + self_response[
        f"round {round - 1}"]

    prefix_string = prefix_string + "\n\nThese are the solutions to the problem from other agents:"
    for i, refer_agent in enumerate(refer_response):
        agent_response = refer_agent[f"round {round - 1}"]
        prefix_string = prefix_string + "\n\n Agent solution" + str(i) + agent_response

    prefix_string = prefix_string + ("\n\nUsing the reasoning from other agents as additional advice with critical "
                                     "thinking, can you give an updated answer? Examine your solution step by step, "
                                     "putting the answer in the form (X) at the end of your response.")

    return [{"role": "user", "content": prefix_string}]


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
    use_model = "gpt-3.5-turbo"
    question_num = 100
    agent_num = 4
    round_num = 3
    test_num = 1

    is_local = True
    if is_local:
        root_path = "D:/01_Study/02_Debate/Selection/code/MMLU"
        questions = json.load(
            open(f"{root_path}/mmlu_row_data/mmlu_random_100.json", "r"))
        output_path = f"{root_path}/mmlu_exp_data/separate/{use_model}_separate_4_3_test1"
    else:
        root_path = "/home/lihaoran/szy/task1"
        questions = json.load(
            open(f"{root_path}/dataset/MMLU/mmlu_random_100.json", "r"))
        output_path = f"{root_path}/exp_data/MMLU/separate/{use_model}_separate_4_3_test1"

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
        agents_response = []

        for agent in range(agent_num):
            agents_response.append({})

        for round in range(round_num):
            print(f"Round {round}")
            for agent in range(agent_num):
                print(f"Agent {agent}")
                agent_prompt = construct_message(agents_response, question, round, agent)
                try:
                    agent_answer = generate_answer(use_model, agent_prompt)
                except openai.BadRequestError as e:
                    error_response_num.append(i)
                    json.dump(error_response_num, open(f"{output_path}/error_response_num.json", "w"))
                    is_error_continue = True
                    break
                agents_response[agent][f"round {round}"] = agent_answer

            if is_error_continue:
                break

        if is_error_continue:
            continue

        generated_description["agents_response"] = agents_response
        json.dump(generated_description, open(f"{save_name}", "w"))
