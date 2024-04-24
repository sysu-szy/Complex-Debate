import os
import json
import time
import random
import openai
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


def construct_message(agents_response, question, round):

    if round == 0:
        prefix_string = random.choice(ROLE_MATH) + "It's a debate to solve the following math problem. \nQuestion: " + question + "\nExplain your reasons at each round thoroughly. Simplify your answer as much as possible. Your final answer should be in the form \\boxed{{answer}}, at the end of your response."
        return [{"role": "user",
                "content": prefix_string}]

    prefix_string = random.choice(ROLE_MATH) + "It's a debate to solve the following math problem. \nQuestion:" + question

    prefix_string = prefix_string + "\n\nThese are the solutions to the problem from other agents:"
    for i, refer_agent in enumerate(agents_response):
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
    content = completion.choices[0].message.content
    time.sleep(2)
    return content


if __name__ == "__main__":
    use_model = "gpt-4"
    question_num = 100
    agent_num = 4
    round_num = 3

    method = "without_individual"
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
        agents_response = []

        for agent in range(agent_num):
            agents_response.append({})

        for round in range(round_num):
            print(f"Round {round}")
            for agent in range(agent_num):
                print(f"Agent {agent}")
                agent_prompt = construct_message(agents_response, question, round)
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

        response_dict["agents_response"] = agents_response

        json.dump(response_dict, open(f"{save_name}", "w"))

