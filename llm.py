import json
import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from config import MODEL
from tools import TOOL_SCHEMAS, TOOLS

load_dotenv()

client = OpenAI(
    base_url=os.environ.get("BASE_URL", "http://localhost:30000/v1"),
    api_key=os.environ.get("API_KEY", "EMPTY"),
)

user_input = input("Enter your prompt> ")

SYSTEM_PROMPT = """
You are a coding agent. Your job is to code. Always code.
Use the bash tool to inspect files.
Answer back to the user once exploration is done.

Your current working directory is: {os.getcwd()}
"""

def call_llm(messages: list, tools: list | None = None):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools or TOOL_SCHEMAS,
    )

    message = response.choices[0].message

    completion_details = response.usage.completion_tokens_details if response.usage else None
    prompt_details = response.usage.prompt_tokens_details if response.usage else None

    usage = {
        "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
        "completion_tokens": response.usage.completion_tokens if response.usage else 0,
        "reasoning_tokens": completion_details.reasoning_tokens if completion_details else 0,
        "cache_tokens": prompt_details.cache_tokens if prompt_details else 0,
    }

    return message, usage

if __name__ == "__main__":
    user_input = input("Enter your prompt> ")

    message, usage = call_llm([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ])

    print("\nAgent: ", message.content, "\n")

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        result = TOOLS[tool_call.function.name](**args)
        print("Tool: ", tool_call.function.name, args)
        print(result, "\n")

    print(usage)