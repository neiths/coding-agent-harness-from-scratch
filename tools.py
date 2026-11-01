import subprocess

from skills import read_skill


def bash(command: str) -> str:
    result = subprocess.run(
        command, 
        shell=True, 
        capture_output=True, 
        text=True, 
        check=False
    )
    return result.stdout + result.stderr


def read_file(path: str) -> str:
    """read a file and return its contents"""
    with open(path) as f:
        return f.read()


def write_file(path: str, content: str) -> str:
    """create a file, or overwrite it if it already exists."""
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {path}"


def str_replace(path: str, old_str: str, new_str: str, allow_multi_edit: bool = False) -> str:
    """Swap exact text in a file. old_str must match exactly once. """
    with open(path) as f:
        content = f.read()
        
    count = content.count(old_str)
    if count == 0:
        return f"Error: old_str was not found in {path}"
    if count > 1 and not allow_multi_edit:
        return (
            f"Error: old_str macthes {count} times in {path}. "
            "Add surrounding lines to make it unique, "
            "or set allow_multi_edit to replace them all."
        )

    with open(path, "w") as f:
        f.write(content.replace(old_str, new_str))

    return f"Replaced {count} match(es) in {path}."


def execute(tool_call):
    """Run one tool call through the permission layer.

    Shared by the main loop and by subagents, so a subagent is fenced in by 
    exactly the same rules - it is not a way around them.

    A tool call is text the model wrote, so all of it is untrusted: the name 
    may not exist, the arguments may not be JSON, and they may not match the signature.
    Every one ofthose comes back  as a result the model can read and retry. 
    None of them is allowed to end the session.
    """

    return None

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command and return its combined stdout and stderr.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to run",
                    }
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a file and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to read",
                    }
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_skill",
            "description": "Read a skill and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the skill to read",
                    }
                },
                "required": ["name"],
            },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "read_skill",
            "description": "Read a skill and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the skill to read",
                    }
                },
                "required": ["name"],
            },
        },
    },
        {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to write to",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file",
                    }
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "str_replace",
            "description": "Replace a string in a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the file to edit",
                    },
                    "old_str": {
                        "type": "string",
                        "description": "The string to replace",
                    },
                    "new_str": {
                        "type": "string",
                        "description": "The string to replace it with",
                    },
                    "allow_multi_edit": {
                        "type": "boolean",
                        "description": (
                            "Whether to allow replacing multiple matches. "
                            "(Default: false)"
                        ),
                    },
                },
                "required": ["path", "old_str", "new_str"],
            },
        },
    },
]


TOOLS = {
    "bash": bash,
    "read_file": read_file,
    "read_skill": read_skill,
    "write_file": write_file,
    "str_replace": str_replace,
}