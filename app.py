import pandas as pd
import gradio as gr
import os

FILE = "tasks.csv"

# ------------------------------
# Load Data (Persistent Storage)
# ------------------------------
if os.path.exists(FILE):
    tasks_df = pd.read_csv(FILE)
else:
    tasks_df = pd.DataFrame(columns=["Task", "Priority", "Due Date", "Status"])


# ------------------------------
# Save Function
# ------------------------------
def save_data():
    tasks_df.to_csv(FILE, index=False)


# ------------------------------
# Add Task
# ------------------------------
def add_task(task, priority, due_date):
    global tasks_df

    new_task = pd.DataFrame({
        "Task": [task],
        "Priority": [priority],
        "Due Date": [due_date],
        "Status": ["Pending"]
    })

    tasks_df = pd.concat([tasks_df, new_task], ignore_index=True)
    save_data()

    return "✅ Task Added!", tasks_df


# ------------------------------
# Complete Task
# ------------------------------
def complete_task(task_name):
    global tasks_df

    if task_name in tasks_df["Task"].values:
        tasks_df.loc[tasks_df["Task"] == task_name, "Status"] = "Completed"
        save_data()
        return f"✅ {task_name} completed!", tasks_df

    return "❌ Task not found!", tasks_df


# ------------------------------
# View Tasks
# ------------------------------
def view_tasks():
    return tasks_df


# ------------------------------
# Generate Study Plan
# ------------------------------
def generate_plan():
    global tasks_df

    pending = tasks_df[tasks_df["Status"] == "Pending"]

    if pending.empty:
        return "🎉 All tasks completed!"

    priority_order = {"High": 1, "Medium": 2, "Low": 3}

    pending = pending.copy()
    pending["Priority Rank"] = pending["Priority"].map(priority_order)
    pending = pending.sort_values(by=["Priority Rank", "Due Date"])

    plan = "📘 Study Plan:\n\n"
    slots = ["Morning", "Afternoon", "Evening"]

    for i, (_, row) in enumerate(pending.iterrows()):
        plan += f"{slots[i % 3]} → {row['Task']} (Due: {row['Due Date']})\n"

    return plan


# ------------------------------
# UI
# ------------------------------
with gr.Blocks() as app:
    gr.Markdown("# 📚 AI Study Planner")

    with gr.Tab("Add Task"):
        task = gr.Textbox(label="Task")
        priority = gr.Dropdown(["High", "Medium", "Low"])
        date = gr.Textbox(label="Due Date")

        btn = gr.Button("Add")
        out = gr.Textbox()
        table = gr.Dataframe()

        btn.click(add_task, [task, priority, date], [out, table])

    with gr.Tab("Complete Task"):
        task_name = gr.Textbox(label="Task Name")
        btn2 = gr.Button("Complete")
        out2 = gr.Textbox()
        table2 = gr.Dataframe()

        btn2.click(complete_task, [task_name], [out2, table2])

    with gr.Tab("View Tasks"):
        btn3 = gr.Button("Refresh")
        table3 = gr.Dataframe()

        btn3.click(view_tasks, outputs=table3)

    with gr.Tab("Generate Plan"):
        btn4 = gr.Button("Generate")
        plan = gr.Textbox(lines=10)

        btn4.click(generate_plan, outputs=plan)


# ------------------------------
# Launch (IMPORTANT)
# ------------------------------
app.launch(server_name="0.0.0.0", server_port=7860)
