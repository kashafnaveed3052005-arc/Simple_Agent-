import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(title: str, due: str = "no due date") -> str:
    tasks = load_tasks()
    tasks.append({"title": title, "due": due, "done": False})
    save_tasks(tasks)
    return f"Added task: {title}"

def list_tasks() -> str:
    tasks = load_tasks()
    if not tasks:
        return "No tasks yet."
    lines = []
    for i, t in enumerate(tasks, 1):
        status = "✅" if t["done"] else "❌"
        lines.append(f"{i}. {t['title']} (due: {t['due']}) {status}")
    return "\n".join(lines)
def complete_task(title: str) -> str:
    tasks = load_tasks()
    for t in tasks:
        if t["title"].lower() == title.lower():
            t["done"] = True
            save_tasks(tasks)
            return f"Marked '{t['title']}' as done."
    return f"Couldn't find a task called '{title}'."

def delete_task(title: str) -> str:
    tasks = load_tasks()
    for t in tasks:
        if t["title"].lower() == title.lower():
            tasks.remove(t)
            save_tasks(tasks)
            return f"Deleted task '{t['title']}'."
    return f"Couldn't find a task called '{title}'."