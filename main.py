import tkinter as tk
from tkinter import messagebox
import json
from functools import partial
from datetime import datetime

SAVE_FILE = "todo_list.json"

# Priority Sorting Helper
PRIORITY_ORDER = {"High": 1, "Medium": 2, "Low": 3}

# Load tasks from the save file
def load_tasks():
    try:
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save tasks to the save file
def save_tasks(tasks):
    with open(SAVE_FILE, "w") as file:
        json.dump(tasks, file)

# Add a new task
def add_task():
    task_name = task_entry.get().strip()
    priority = priority_var.get()
    deadline = deadline_entry.get().strip()

    if not task_name:
        messagebox.showwarning("Input Error", "Task name cannot be empty!")
        return

    if deadline:
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid date format! Use YYYY-MM-DD.")
            return

    tasks.append({"name": task_name, "priority": priority, "deadline": deadline, "completed": False})
    save_tasks(tasks)
    update_task_list()
    task_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)

# Remove a task
def remove_task(index):
    tasks.pop(index)
    save_tasks(tasks)
    update_task_list()

# Mark a task as complete
def mark_complete(index):
    tasks[index]["completed"] = True
    save_tasks(tasks)
    update_task_list()

# Sort tasks by priority and completion status
def sort_tasks():
    tasks.sort(key=lambda x: (x["completed"], PRIORITY_ORDER[x["priority"]], x["deadline"] or ""))

# Filter tasks based on the current filter type
def filter_tasks(filter_type):
    global current_filter
    current_filter = filter_type
    update_task_list()

# Update the task list in the GUI
def update_task_list():
    sort_tasks()

    for widget in task_frame.winfo_children():
        widget.destroy()

    for index, task in enumerate(tasks):
        if current_filter == "Completed" and not task["completed"]:
            continue
        if current_filter == "Pending" and task["completed"]:
            continue

        task_text = f"{task['name']} ({task['priority']})"
        if task["deadline"]:
            today = datetime.today().strftime("%Y-%m-%d")
            if task["deadline"] < today and not task["completed"]:
                task_text += f" [Overdue: {task['deadline']}]"
            elif task["deadline"] >= today and not task["completed"]:
                task_text += f" [Due: {task['deadline']}]"

        if task["completed"]:
            task_text += " ✓"

        task_label = tk.Label(task_frame, text=task_text, anchor="w")
        task_label.pack(fill="x", padx=5, pady=2)

        if not task["completed"]:
            complete_button = tk.Button(task_frame, text="Complete", command=partial(mark_complete, index))
            complete_button.pack(side="right", padx=5)

        remove_button = tk.Button(task_frame, text="Remove", command=partial(remove_task, index))
        remove_button.pack(side="right", padx=5)

# Global variables for tasks and filter
tasks = load_tasks()
current_filter = "All"

# GUI Setup
root = tk.Tk()
root.title("Enhanced Todo List App")

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

task_entry = tk.Entry(input_frame, width=25)
task_entry.pack(side="left", padx=5)
task_entry.insert(0, "Task Name")

deadline_entry = tk.Entry(input_frame, width=15)
deadline_entry.pack(side="left", padx=5)
deadline_entry.insert(0, "YYYY-MM-DD")

priority_var = tk.StringVar(value="Medium")
priority_menu = tk.OptionMenu(input_frame, priority_var, "High", "Medium", "Low")
priority_menu.pack(side="left", padx=5)

add_button = tk.Button(input_frame, text="Add Task", command=add_task)
add_button.pack(side="left", padx=5)

# Filter Frame
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

filter_label = tk.Label(filter_frame, text="Filter Tasks:")
filter_label.pack(side="left", padx=5)

all_button = tk.Button(filter_frame, text="All", command=lambda: filter_tasks("All"))
all_button.pack(side="left", padx=5)

pending_button = tk.Button(filter_frame, text="Pending", command=lambda: filter_tasks("Pending"))
pending_button.pack(side="left", padx=5)

completed_button = tk.Button(filter_frame, text="Completed", command=lambda: filter_tasks("Completed"))
completed_button.pack(side="left", padx=5)

# Task List Frame
task_frame = tk.Frame(root)
task_frame.pack(pady=10, fill="x")

update_task_list()

# Start the GUI loop
root.mainloop()
