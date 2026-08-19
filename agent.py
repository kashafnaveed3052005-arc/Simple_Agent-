import ollama
from tasks import add_task, list_tasks, complete_task, delete_task

# --- Describe each tool so the model knows what it can do ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the to-do list",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The task description"},
                    "due": {"type": "string", "description": "Due date, e.g. 'tomorrow', 'Friday'. Optional."}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all current tasks",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as done by its title",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The exact or closest matching task title"}
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by its title",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The exact or closest matching task title"}
                },
                "required": ["title"]
            }
        }
    }
]

# Map tool name -> actual Python function
available_functions = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
}

def run_agent(user_input: str):
    messages = [{"role": "user", "content": user_input}]

    # 1st model call to determine if function calling is needed
    # Change from "llama3.1:8b" to "llama3.2:3b"
    response = ollama.chat(model="llama3.2:3b", messages=messages, tools=tools)
    messages.append(response["message"])

    # If the model requested tool calls
    if response["message"].get("tool_calls"):
        for call in response["message"]["tool_calls"]:
            fn_name = call["function"]["name"]
            fn_args = call["function"]["arguments"]
            print(f"[agent is calling tool: {fn_name}({fn_args})]")

            # Execute local Python function
            if fn_name in available_functions:
                result = available_functions[fn_name](**fn_args)

                # Return function response as string to the context window
                messages.append({
                    "role": "tool",
                    "content": str(result),
                    "name": fn_name
                })

        # 2nd model call using the aggregated results to answer the user
        final_response = ollama.chat(model="llama3.2:3b", messages=messages)
        return final_response["message"]["content"]

    return response["message"]["content"]

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() in ("exit", "quit"):
            break
        if not user_input.strip():
            continue
        answer = run_agent(user_input)
        print("Agent:", answer)