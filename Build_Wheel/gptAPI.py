from openai import OpenAI
from enum import Enum
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from nltk.tokenize import sent_tokenize
import nltk
import re
import os
import random

class Clients(Enum):
    client_free = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="sk-PMSqPTJgxZqpgF8onvnsbEfPUYPk7WYHzfBCOx4eY3tjPc2u",
        base_url="https://api.chatanywhere.tech/v1"
    )

    client_paid = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key="sk-5pzatlsS3ukKWKdQ8TW40Z5BhnS8UW5rEcdzeSndTGxvmKH9",
        base_url="https://api.chatanywhere.tech/v1"
    )

class Model(Enum):
    gpt35t          = "gpt-3.5-turbo"
    gpt4            = "gpt-4"
    gpt4o           = "gpt-4o"
    # 上述模型对免费版客户端可用，gpt4以及gpt4o一天共计可用三次
    gpt35t_ca       = "gpt-3.5-turbo-ca"
    gpt4t           = "gpt-4-turbo"
    gpt4o_ca        = "gpt-4o-ca"
    gpt4t_ca        = "gpt-4-turbo-ca"
    gpt4t_prev_ca   = "gpt-4-turbo-preview-ca"
    # 上述模型对付费版均可用


# 非流式响应
def gpt_api(Client: Clients, Model: Model, messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = (Client.value).chat.completions.create(model=Model.value, messages=messages)
    print(completion.choices[0].message.content)

def gpt_api_stream(Client: Clients, Model: Model, messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    stream = (Client.value).chat.completions.create(
        model=Model.value,
        messages=messages,
        stream=True,
    )
    ans = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            ans += chunk.choices[0].delta.content
    print("\n")
    return ans

def Data_quality_assessment(Client: Clients, Model: Model, File_path):
    # 使用with语句自动管理文件的打开和关闭
    with open(File_path, 'r', encoding='utf-8') as file:
        content = file.read()  # 读取整个文件内容

    vuln_num_pattern = r'CVE-\d{4}-\d{4}'
    vuln_num = re.search(vuln_num_pattern, file.name).group()

    messages = [{'role': 'user',
                 'content': '请分析:' + content + '该内容是否与漏洞:' + vuln_num 
                          + '的描述信息或其POC(Proof Of Concept)信息相关?\n'
                          + '注：输出格式如下\n'
                          + '描述信息：(有/无)关'
                          + 'POC信息：(有/无)关'
                          + '内容概述：(对上述给出的内容作简要分析概述)'},]
    # 非流式调用
    # gpt_api(Client, Model, messages)
    # 流式调用
    return gpt_api_stream(Client, Model, messages)

def Common_Chat(Client: Clients, Model: Model, Messages):
    messages = []
    for Message in Messages:
        messages.append({'role': 'user','content': Message})
    # 非流式调用
    # gpt_35_api(Client, Model, messages)
    # 流式调用
    gpt_api_stream(Client, Model, messages)

def count_tokens_in_file(file_path, tokenizer, model_max_length=1024):
    nltk.download('punkt')
    token_count = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().strip()
        # 使用nltk进行句子分割
        sentences = sent_tokenize(text)
        for sentence in sentences:
            if len(tokenizer.encode(sentence, return_tensors='pt')) > model_max_length:
                # 如果单个句子超过最大长度，进行进一步分割
                while len(tokenizer.encode(sentence, return_tensors='pt')) > model_max_length:
                    sentence = sentence[:-10]  # 简化的分割逻辑，实际应用中可能需要更精细的处理
            encoded_sentence = tokenizer(sentence, return_tensors='pt')
            token_count += len(encoded_sentence['input_ids'][0])
    return token_count

    