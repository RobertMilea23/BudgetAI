# Python AI Agent

A local AI agent powered by an LLM (Google Gemini) that can autonomously read, write, and execute Python files within a sandboxed working directory.

## Features

- Browse and inspect files in a working directory
- Read file contents
- Write and overwrite files
- Execute Python scripts with optional arguments
- 30-second execution timeout for safety
- Restricted to a single working directory to limit scope

## How It Works

The agent receives a user prompt and iteratively calls tools (functions) to complete the task. It uses the Gemini API to decide which tools to call and what arguments to pass. The loop continues until the LLM produces a final response with no further tool calls.

### Available Tools

| Tool | Description |
|---|---|
| `get_files_info` | List files in a directory |
| `get_file_content` | Read the contents of a file |
| `write_file` | Write content to a file |
| `run_python_file` | Execute a Python file with optional arguments |

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/python-ai-agent.git
   cd python-ai-agent
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Set your Gemini API key:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

4. Run the agent:
   ```bash
   uv run main.py "your prompt here"
   ```


This project is for **learning purposes only**. The agent can execute arbitrary Python code within the working directory. Do not expose this to untrusted users or use it in a production environment.
