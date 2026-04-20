import pandas as pd
import gradio as gr

# ------------------------------
# Data Storage (in-memory)
# ------------------------------
tasks_df = pd.DataFrame(columns=["Task", "Priority", "Due Date", "Status"])

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
    return "Task Added Successfully!", tasks_df


# ------------------------------
# Complete Task
# ------------------------------
def complete_task(task_name):
    global tasks_df

    if task_name in tasks_df["Task"].values:
        tasks_df.loc[tasks_df["Task"] == task_name, "Status"] = "Completed"
        return f"Task '{task_name}' marked as completed.", tasks_df
    else:
        return "Task not found!", tasks_df


# ------------------------------
# View Tasks
# ------------------------------
def view_tasks():
    return tasks_df


# ------------------------------
# AI Study Plan Generator
# ------------------------------
def generate_plan():
    global tasks_df

    if tasks_df.empty:
        return "No tasks available."

    pending = tasks_df[tasks_df["Status"] == "Pending"]

    if pending.empty:
        return "All tasks completed 🎉"

    priority_order = {"High": 1, "Medium": 2, "Low": 3}

    pending = pending.copy()
    pending["Priority Rank"] = pending["Priority"].map(priority_order)
    pending = pending.sort_values(by=["Priority Rank", "Due Date"])

    plan = "📘 AI Study Plan:\n\n"
    time_slots = ["9 AM - 12 PM", "1 PM - 4 PM", "6 PM - 9 PM"]

    for i, (_, row) in enumerate(pending.iterrows()):
        slot = time_slots[i % len(time_slots)]
        plan += f"{slot}: {row['Task']} (Priority: {row['Priority']}, Due: {row['Due Date']})\n"

    return plan


# ------------------------------
# UI
# ------------------------------
with gr.Blocks() as app:

    gr.Markdown("# 📚 AI-Based Study Planner")

    with gr.Tab("➕ Add Task"):
        task_input = gr.Textbox(label="Task Name")
        priority_input = gr.Dropdown(["High", "Medium", "Low"])
        due_date_input = gr.Textbox(label="Due Date (YYYY-MM-DD)")

        add_btn = gr.Button("Add Task")
        add_output = gr.Textbox()
        table_output = gr.Dataframe()

        add_btn.click(add_task, inputs=[task_input, priority_input, due_date_input],
                      outputs=[add_output, table_output])

    with gr.Tab("✅ Complete Task"):
        complete_input = gr.Textbox(label="Task Name")
        complete_btn = gr.Button("Mark Complete")
        complete_output = gr.Textbox()
        complete_table = gr.Dataframe()

        complete_btn.click(complete_task, inputs=[complete_input],
                           outputs=[complete_output, complete_table])

    with gr.Tab("📋 View Tasks"):
        view_btn = gr.Button("Refresh")
        view_table = gr.Dataframe()

        view_btn.click(view_tasks, outputs=view_table)

    with gr.Tab("🧠 Generate Study Plan"):
        plan_btn = gr.Button("Generate Plan")
        plan_output = gr.Textbox(lines=15)

        plan_btn.click(generate_plan, outputs=plan_output)


# IMPORTANT for deployment
app.launch(server_name="0.0.0.0", server_port=7860)