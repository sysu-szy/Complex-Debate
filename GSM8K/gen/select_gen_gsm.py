from openai import OpenAI
import time
import json
import random
import os

ROLE_MATH = ["You are a super-intelligent AI assistant capable of performing tasks more effectively than humans.",
             "You are a mathematician. You are good at math games, arithmetic calculation, and long-term planning.",
             "You are an expert in the field of algebra, skilled at solving equations, understanding variables and adept at the logical manipulation of symbols.",
             "You specialize in the realm of counting and probability, able to calculate complex events with accuracy, analyze data and predict outcomes.",
             "You are a wizard of geometry, deeply familiar with shapes, dimensions, and properties, and capable of theorizing spatial relationships and understanding geometric proofs.",
             "You are a maestro of intermediate algebra, adept at handling polynomials, quadratic equations, and dealing with complex numerical relationships.",
             "As a scholar in number theory, you excel in studying properties and relationships of numbers. Prime numbers, divisibility, and mathematical patterns are within your area of expertise.",
             "You are a prodigy in prealgebra, skillful at understanding mathematical principles and fundamentals like operations, fractions, and basic equations.",
             "You are a guru in precalculus, proficient at handling functions, limits, rates of change, and confidently preparing for the concepts of calculus."]

def read_jsonl(path: str):
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]


def save_random_question(question_num):
    questions = read_jsonl("/dataset/GSM8K/grade_school_math/data/test.jsonl")
    output_path = f"D:/01_Study/02_Debate/Selection/code/GSM8K/gsm_row_data/gsm_random_{question_num}.json"

    random.seed(0)
    random.shuffle(questions)
    random_questions = {}
    for i, data in enumerate(questions[:question_num]):
        question = data['question']
        answer = data['answer']
        random_questions[str(i)] = (question, answer)

    json.dump(random_questions, open(f"{output_path}", "w"))

def construct_message(agents_response, question, round, agent):
    refer_response = agents_response[0:agent] + agents_response[agent + 1:]
    self_response = agents_response[agent]

    if round == 0:
        prefix_string = random.choice(ROLE_MATH) + "It's a debate to solve the following math problem. \nQuestion: " + question + "\nExplain your reasons at each round thoroughly. Your final answer should be a single numerical number, in the form \\boxed{{answer}}, at the end of your response."
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
                                     "Your final answer should be a single numerical number, in the form \\boxed{{"
                                     "answer}}, at the end of your response.")

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
    test_num = 1

    root_path = "D:/01_Study/02_Debate/Selection/code/GSM8K"
    questions = json.load(open(f"{root_path}/gsm_row_data/gsm_random_100.json", "r"))
    output_path = f"{root_path}/gsm_exp_data/separate/{use_model}_separate_4_3_test1"

    for i in range(question_num):
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
                agent_answer = generate_answer(use_model, agent_prompt)
                agents_response[agent][f"round {round}"] = agent_answer

        generated_description["agents_response"] = agents_response

        json.dump(generated_description, open(f"{save_name}", "w"))
