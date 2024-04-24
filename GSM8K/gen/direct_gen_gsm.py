from openai import OpenAI
import json
import random


def read_jsonl(path: str):
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]


if __name__ == "__main__":
    use_model = "gpt-4"
    question_num = 5
    test_num = 1

    random.seed(0)
    generated_description = {}

    questions = read_jsonl("/dataset/GSM8K/grade_school_math/data/test.jsonl")
    output_path = f"D:\\01_Study\\02_Debate\\Selection\\code\\GSM8K\\gsm_exp_data\\direct\\{use_model}_direct_gsm_{question_num}_test{test_num}"
    random.shuffle(questions)

    for i, data in enumerate(questions[:question_num]):
        question = data['question']
        answer = data['answer']

        context = [{"role": "user",
                    "content": """Can you solve the following math problem? {} Explain your reasoning. Your final answer should be a single numerical number, in the form \\boxed{{answer}}, at the end of your response. """.format(
                        question)}]

        client = OpenAI()
        completion = client.chat.completions.create(
            model=use_model,
            messages=context,
        )
        time.sleep(5)
        ans_content = completion.choices[0].message.content

        print(f"question {i}: {question}")
        print(f"agent_answer {i}: {ans_content}")
        print("\n")
        generated_description[question] = (i, ans_content, answer)

    json.dump(generated_description, open(f"{output_path}.json", "w"))
