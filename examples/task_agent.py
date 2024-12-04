"""
任务管理智能体示例
"""

import os
import json

from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

load_dotenv() 


def invoke_chat_model(system_prompt, user_prompt, tool_config):
    client = Ark(
            api_key=os.environ.get("ARK_API_KEY"),
            base_url="https://ark.cn-beijing.volces.com/api/v3"
    )
    chat_completion_params = {
            "model": os.environ.get("ARK_ENDPOINT_ID"),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.8,
            "tools": [
                {
                    "type": "function",
                    "function": tool_config
                }
            ]
        }
    response = client.chat.completions.create(**chat_completion_params).model_dump()
    choices = response.get("choices")
    if choices and len(choices) > 0:
        first_choice = choices[0]
        # 尝试解析 tool_calls
        if ('message' in first_choice and 
            'tool_calls' in first_choice['message'] and 
            first_choice['message']['tool_calls'] is not None and
            len(first_choice['message']['tool_calls']) > 0):
            tool_call = first_choice['message']['tool_calls'][0]
            return json.loads(tool_call['function']['arguments'])
        # 如果无法解析 tool_calls，返回原始消息内容
        elif 'message' in first_choice:
            return first_choice['message']
    return None


def invoke_task_secretary():
    system_prompt = """
    你是任务管理书记员。
    请分析用户提供的信息与要求提炼任务标题和描述，使用给出的工具函数`create_task`创建任务。
    """
    user_prompt = """
发言者：阿木
原文 ：@小舟 我已经给客户发了，你把更新的给客户，并更新我提交的文件。
补充 1：“文件”指的是分类标记数据文件。
补充 2： 我已经给客户发过一份，并且在微盘存了一份。
"""
    tool_config = {
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
                },
                "owner": {
                    "type": "string",
                    "description": "任务负责人"
                },
                "reviewer": {
                    "type": "string",
                    "description": "任务复核人"
                }
            },
            "required": ["title", "description", "owner", "reviewer"]
        }
    }
    result = invoke_chat_model(system_prompt, user_prompt, tool_config)
    return result


if __name__ == "__main__":
    task = invoke_task_secretary()
    print(task)
    # 输出结果
    # {'description': '阿木已给客户发过一份分类标记数据文件且在微盘存一份，让小舟给客户发送更新的文件并更新阿木提交的分类标记数据文件。', 
    # 'owner': '阿木', 'reviewer': '小舟', 
    # 'title': '阿木安排小舟发送更新文件并更新提交文件'}