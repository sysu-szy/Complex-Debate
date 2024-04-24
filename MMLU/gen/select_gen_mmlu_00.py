from glob import glob
import pandas as pd
import json
import time
import random
from openai import OpenAI

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
    client = OpenAI()
    completion = client.chat.completions.create(
        model=use_model,
        messages=context,
    )
    time.sleep(5)
    return completion.choices[0].message.content


if __name__ == "__main__":
    use_models = ["gpt-4"]
    question_num = 100
    agent_num = 4
    round_num = 3
    test_num = 1

    root_path = "/home/lihaoran/szy/task1/"

    for use_model in use_models:

        tasks = glob(f"{root_path}/dataset/MMLU/test/*.csv")
        output_path = f"{root_path}/exp_data/MMLU/select/{use_model}_select_mmlu_{question_num}_{agent_num}_{round_num}_test{test_num}"
        dfs = [pd.read_csv(task) for task in tasks]

        random.seed(0)
        generated_description = {}

        for i in range(question_num):
            print("\n", f"Question {i}")
            len_dfs = len(dfs)
            idfs = random.randint(0, len_dfs - 1)
            df = dfs[idfs]
            ix = len(df)
            idx = random.randint(0, ix - 1)

            question, answer = parse_question_answer(df, idx)
            agents_response = []

            for agent in range(agent_num):
                agents_response.append({})

            for round in range(round_num):
                print(f"Round {round}")
                for agent in range(agent_num):
                    print(f"Agent {agent}")
                    agent_prompt = construct_message(agents_response, question, round, agent)
                    agent_answer = generate_answer(use_model, agent_prompt)
                    agents_response[agent][f"round {round}"] = agent_answer

            generated_description[question] = (i, agents_response, answer)

        json.dump(generated_description, open(f"{output_path}.json", "w"))
