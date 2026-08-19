# Simple AI Agent - To-Do List Manager

A lightweight, Python-powered AI agent designed to automate and manage daily tasks efficiently. This project demonstrates basic agentic workflows by structuring, executing, and persisting to-do list tasks programmatically.

---

##  Features

- **Automated Task Management:** Create, track, and structure tasks dynamically.
- **Persistent Data Storage:** Stores and loads task states using JSON for seamless execution across sessions.
- **Modular Design:** Clear separation of agent reasoning (`agent.py`) and task execution logic (`tasks.py`).

---```bash

##  Repository Structure

```text
├── agent.py          # Core AI agent logic and decision loop
├── tasks.py          # Functions for task handling (CRUD operations)
├── tasks.json        # Local storage for saved tasks
├── .gitignore        # Ignores unwanted files (e.g., __pycache__)
└── README.md         # Project documentation