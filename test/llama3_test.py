from langchain_community.llms import Ollama

if __name__ == '__main__':
    # 替换成你的Llama3模型路径
    llm = Ollama(model="llama3")
    llm.invoke("Why is the sky blue?")