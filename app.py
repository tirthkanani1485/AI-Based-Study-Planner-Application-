import streamlit as st
import pandas as pd
import os

# ------------------------------
# File Storage
# ------------------------------
FILE = "tasks.csv"

# Load data
if os.path.exists(FILE):
    tasks_df = pd.read_csv(FILE)
else:
    tasks_df = pd.DataFrame(columns=["Task", "Priority", "Due Date", "Status"])

# Save function
def save_data():
    tasks_df.to_csv(FILE, index=False)

# ------------------------------
# UI Title
# ------------------------------
st.title("📚 AI-Based Study Planner")

# ------------------------------
# Sidebar Navigation
# ------------------------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Task", "Complete Task", "View Tasks", "Generate Plan"]
)

# ------------------------------
# Add Task
# ------------------------------
if menu == "Add Task":
    st.subheader("➕ Add New Task")

    task = st.text_input("Task Name")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("Due Date")

    if st.button("Add Task"):
        if task:
            new_task = pd.DataFrame({
                "Task": [task],
                "Priority": [priority],
                "Due Date": [str(due_date)],
                "Status": ["Pending"]
            })

            tasks_df = pd.concat([tasks_df, new_task], ignore_index=True)
            save_data()

            st.success("✅ Task Added Successfully!")
        else:
            st.error("❌ Please enter task name")

# ------------------------------
# Complete Task
# ------------------------------
elif menu == "Complete Task":
    st.subheader("✅ Mark Task Complete")

    task_name = st.text_input("Enter Task Name")

    if st.button("Complete Task"):
        if task_name in tasks_df["Task"].values:
            tasks_df.loc[tasks_df["Task"] == task_name, "Status"] = "Completed"
            save_data()
            st.success(f"✅ {task_name} marked as completed")
        else:
            st.error("❌ Task not found")

# ------------------------------
# View Tasks
# ------------------------------
elif menu == "View Tasks":
    st.subheader("📋 All Tasks")

    if tasks_df.empty:
        st.info("No tasks available")
    else:
        st.dataframe(tasks_df)

# ------------------------------
# Generate Study Plan
# ------------------------------
elif menu == "Generate Plan":
    st.subheader("🧠 AI Study Plan")

    pending = tasks_df[tasks_df["Status"] == "Pending"]

    if pending.empty:
        st.success("🎉 All tasks completed!")
    else:
        priority_order = {"High": 1, "Medium": 2, "Low": 3}

        pending = pending.copy()
        pending["Priority Rank"] = pending["Priority"].map(priority_order)
        pending = pending.sort_values(by=["Priority Rank", "Due Date"])

        time_slots = ["Morning", "Afternoon", "Evening"]

        st.write("### 📘 Your Study Plan:")

        for i, (_, row) in enumerate(pending.iterrows()):
            st.write(
                f"👉 {time_slots[i % 3]} → {row['Task']} "
                f"(Priority: {row['Priority']}, Due: {row['Due Date']})"
            )

# ------------------------------
# Footer
# ------------------------------
st.sidebar.markdown("🚀 Made with Streamlit")
