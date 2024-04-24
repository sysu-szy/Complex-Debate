import json
import time
import os
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

if __name__ == '__main__':
    data = json.load(open("D:/01_Study/02_Debate/Selection/code/test/thoughts.json", "r"))
    use_model = "gpt-4"
    gpt_responses = []
    for i in range(len(data)):
        print("Question:", i)
        response = generate_answer(use_model, data[i])
        gpt_responses.append(response)
    json.dump(gpt_responses, open("D:/01_Study/02_Debate/Selection/code/test/responses.json", "w"))

    """
    我已经跑好并保存结果了啦，想要看responses的话，直接运行下面的代码就行了
    responses = json.load(open("D:/01_Study/02_Debate/Selection/code/test/responses.json", "r"))    # 这是responses.json的文件保存地址
    for i in range(len(responses)):
        print(responses[i])
    """




