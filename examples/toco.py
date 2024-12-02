"""
TOCO as Example Agent 
"""
import os
import time
import json

from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark


SYSTEM_PROMPT = """
你是TOCO，一个任务管理助手。
请分析用户提供的信息与要求提炼任务标题和描述，使用给出的工具函数`create_task`创建任务。
"""

load_dotenv() 


def create_task(title:str, description:str):
    return {'title': title, 'description': description}


class TOCO:
    def __init__(self, input_std):
        self.client = Ark(
            api_key=os.environ.get("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        )
        self.chat_completion_params = {
            "model": os.environ.get("ARK_ENDPOINT_ID"),
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": input_std}
            ],
            "temperature": 0.8,
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "create_task",
                        "description": "创建任务",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "任务标题"
                                },
                                "description": {
                                    "type": "string",
                                    "description": "任务描述"
                                }
                            },
                            "required": ["title", "description"]
                        }
                    }
                }
            ]
        }
    
    def match(self, debug=False):
        response = self.client.chat.completions.create(**self.chat_completion_params).model_dump()
        if debug:
            return json.dumps(response, indent=2, ensure_ascii=False)
        else:
            if response.get("choices")[0].get("message").get("tool_calls"):
                return response.get("choices")[0].get("message").get("tool_calls")[0].get("function").get("arguments")
            return self.match(debug)


def main():
    timer = time.time()
    input_std = "我想帮助我的同事把项目策划书给写了。这个策划书的主要内容是介绍数据处理流程。"
    doubao_chat = TOCO(input_std)
    # 调试模式(原始文本输出)
    result_debug = doubao_chat.match(debug = True)
    print("Debug mode result (原始文本):")
    print(result_debug)
    # 结果
    # title: 帮助同事写项目策划书
    # description: 帮助同事写一个主要介绍数据处理流程的项目策划书


if __name__ == "__main__":
    main()
