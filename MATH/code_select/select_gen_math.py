import pandas as pd
import os
import json
import time
import random
from openai import OpenAI

ROLE_MATH = ["You are a super-intelligent AI assistant capable of performing tasks more effectively than humans.",
             "You are a mathematician. You are good at math games, arithmetic calculation, and long-term planning.",
             "You are an expert in the field of algebra, skilled at solving equations, understanding variables and adept at the logical manipulation of symbols.",
             "You specialize in the realm of counting and probability, able to calculate complex events with accuracy, analyze data and predict outcomes.",
             "You are a wizard of geometry, deeply familiar with shapes, dimensions, and properties, and capable of theorizing spatial relationships and understanding geometric proofs.",
             "You are a maestro of intermediate algebra, adept at handling polynomials, quadratic equations, and dealing with complex numerical relationships.",
             "As a scholar in number theory, you excel in studying properties and relationships of numbers. Prime numbers, divisibility, and mathematical patterns are within your area of expertise.",
             "You are a prodigy in prealgebra, skillful at understanding mathematical principles and fundamentals like operations, fractions, and basic equations.",
             "You are a guru in precalculus, proficient at handling functions, limits, rates of change, and confidently preparing for the concepts of calculus."]

def save_random_question(question_num):
    levels = ["level1", "level2", "level3", "level4", "level5"]

    for level in levels:
        data_path = f"D:\\01_Study\\02_Debate\\Selection\\code\\MATH\\math_row_data\\level\\{level}"

        output_path = "D:\\01_Study\\02_Debate\\Selection\\code\\MATH\\math_row_data\\random_questions"
        if not os.path.exists(f"{output_path}\\{level}"):
            os.makedirs(f"{output_path}\\{level}")
        output_path = f"{output_path}\\{level}\\math_random_{question_num}"

        random.seed(0)
        tasklist = os.listdir(f"{data_path}")
        random_questions = {}

        for i in range(question_num):
            print('\n', f"Question {i}")
            question_name = random.choice(tasklist)

            subject_question = json.load(open(f"{data_path}\\{question_name}"))
            question = subject_question["problem"]
            answer = subject_question["solution"]
            random_questions[str(i)] = (question, answer)

        json.dump(random_questions, open(f"{output_path}.json", "w"))

def construct_message(agents_response, question, round, agent):
    refer_response = agents_response[0:agent] + agents_response[agent + 1:]
    self_response = agents_response[agent]

    if round == 0:
        prefix_string = random.choice(ROLE_MATH) + "It's a debate to solve the following math problem. \nQuestion: " + question + "\nExplain your reasons at each round thoroughly. Simplify your answer as much as possible. Your final answer should be in the form \\boxed{{answer}}, at the end of your response."
        return [{"role": "user",
                "content": prefix_string}]

    prefix_string = random.choice(ROLE_MATH) + "It's a debate to solve the following math problem. \nQuestion:" + question

    prefix_string = prefix_string + "\n\nIt's your solution from the last round:\n" + self_response[
        f"round {round - 1}"]

    prefix_string = prefix_string + "\n\nThese are the solutions to the problem from other agents:"
    for i, refer_agent in enumerate(refer_response):
        agent_response = refer_agent[f"round {round - 1}"]
        prefix_string = prefix_string + "\n\n Agent solution" + str(i) + agent_response

    prefix_string = prefix_string + ("\n\nUsing the reasoning from other agents as additional advice with critical "
                                     "thinking, can you give an updated answer? Examine your solution step by step. "
                                     "Simplify your answer as much as possible. Your final answer should be in the "
                                     "form \\boxed{{answer}}, at the end of your response.")

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
    use_model = "gpt-3.5-turbo"
    level = "level1"
    question_num = 3
    agent_num = 4
    round_num = 3
    test_num = 1

    data_path = f"D:\\01_Study\\02_Debate\\Selection\\code\\MATH\\math_row_data\\level\\{level}"

    output_path = "D:\\01_Study\\02_Debate\\Selection\\code\\MATH\\math_exp_data\\select"

    if not os.path.exists(f"{output_path}\\{level}"):
        os.makedirs(f"{output_path}\\{level}")
    if not os.path.exists(f"{output_path}\\{level}\\response"):
        os.makedirs(f"{output_path}\\{level}\\response")
    if not os.path.exists(f"{output_path}\\{level}\\accurate"):
        os.makedirs(f"{output_path}\\{level}\\accurate")
    output_path = f"{output_path}\\{level}\\response\\{use_model}_direct_math_{question_num}_{agent_num}_{round_num}_test{test_num}"

    random.seed(0)
    response_dict = {}
    tasklist = os.listdir(f"{data_path}")

    for i in range(question_num):
        print('\n', f"Question {i}")
        question_name = random.choice(tasklist)

        subject_question = json.load(open(f"{data_path}\\{question_name}"))
        question = subject_question["problem"]
        answer = subject_question["solution"]
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

        response_dict[question] = (i, agents_response, answer)

    json.dump(response_dict, open(f"{output_path}.json", "w"))
