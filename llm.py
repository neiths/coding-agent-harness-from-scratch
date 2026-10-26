import json
import os
import subprocess

from dotenv import load_dotenv
from openai import OpenAI

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
"""

BASH_TOOL = {
    "type": "function",
    "function": {
        "name": "bash",
        "description": "Run a shell command and return its output.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to run.",
                },
            },
            "required": ["command"],
        },
    },
}

def bash(command: str) -> str:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout + result.stderr

model = os.environ.get("MODEL", "Qwen/Qwen3-0.6B")
response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ],
    tools=[BASH_TOOL],
)

message = response.choices[0].message
output = message.content

completion_details = getattr(response.usage, "completion_tokens_details", None) if response.usage else None
prompt_details = getattr(response.usage, "prompt_tokens_details", None) if response.usage else None

usage = {
    "completion_tokens": getattr(response.usage, "completion_tokens", 0) if response.usage else 0,
    "prompt_tokens": getattr(response.usage, "prompt_tokens", 0) if response.usage else 0,
    "reasoning_tokens": getattr(completion_details, 'reasoning_tokens', 0) if completion_details else 0,
    "cache_tokens": getattr(prompt_details, 'cache_tokens', 0) if prompt_details else 0,
}

breakpoint()  # Debugging point to inspect variables
print("\nAgent: ", output, "\n")

if message.content:
    import re
    text = message.content
    match = re.search(r'<tool_call>(.*?)</tool_call>', text, re.DOTALL)
    if match:
        print(match.group(1).strip())
        command = json.loads(match.group(1).strip())["arguments"]["command"]
        # print("Tool: bash", command)
        # print(bash(command), "\n")

# if message.tool_calls:
#     tool_call = message.tool_calls[0]
#     command = json.loads(tool_call.arguments)["command"]
#     print("Tool: bash", command)
#     print(bash(command), "\n")

print("Usage:", json.dumps(usage, indent=2))