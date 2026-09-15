import streamlit as st
from datetime import date

from database.database import (
    create_table,
    add_task,
    get_tasks,
    update_task_status
)


# --------------------------------
# Create Database Tables
# --------------------------------

create_table()


# --------------------------------
# Page Title
# --------------------------------

st.title("📝 Study Planner")

st.write(
    "Plan your study tasks, manage priorities, "
    "and keep track of your progress."
)


# --------------------------------
# Add New Task
# --------------------------------

st.subheader("➕ Add New Task")

with st.form("task_form"):

    subject = st.text_input(
        "Subject",
        placeholder="e.g. Data Structures"
    )

    topic = st.text_input(
        "Topic / Task",
        placeholder="e.g. Binary Search"
    )

    col1, col2 = st.columns(2)

    with col1:

        priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"]
        )

    with col2:

        planned_date = st.date_input(
            "Planned Date",
            date.today()
        )

    planned_duration = st.number_input(
        "Planned Study Duration (minutes)",
        min_value=15,
        max_value=600,
        value=60,
        step=15
    )

    deadline = st.date_input(
        "Deadline",
        date.today()
    )

    submitted = st.form_submit_button(
        "➕ Add Task"
    )


    # --------------------------------
    # Add Task
    # --------------------------------

    if submitted:

        if not subject:

            st.error(
                "Please enter the subject."
            )

        elif not topic:

            st.error(
                "Please enter the topic or task."
            )

        elif deadline < planned_date:

            st.error(
                "⚠️ Deadline cannot be before the planned date."
            )

        else:

            add_task(
                subject,
                topic,
                priority,
                planned_date,
                planned_duration,
                deadline
            )

            st.success(
                f"🎉 Task '{topic}' added successfully!"
            )

            st.rerun()


# --------------------------------
# Task List
# --------------------------------

st.divider()

st.subheader("📋 My Tasks")

tasks = get_tasks()


# --------------------------------
# Task Statistics
# --------------------------------

total_tasks = len(tasks)

completed_tasks = sum(
    1
    for task in tasks
    if task[7] == "Completed"
)

pending_tasks = total_tasks - completed_tasks

overdue_tasks = 0

for task in tasks:

    deadline = date.fromisoformat(task[6])
    status = task[7]

    if deadline < date.today() and status == "Pending":

        overdue_tasks += 1


col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📚 Total Tasks",
        total_tasks
    )

with col2:

    st.metric(
        "⏳ Pending",
        pending_tasks
    )

with col3:

    st.metric(
        "✅ Completed",
        completed_tasks
    )

with col4:

    st.metric(
        "⚠️ Overdue",
        overdue_tasks
    )


# --------------------------------
# Filters
# --------------------------------

if tasks:

    st.divider()

    st.subheader("🔍 Find Tasks")

    col1, col2, col3 = st.columns(3)

    with col1:

        search_text = st.text_input(
            "Search",
            placeholder="Search subject or topic..."
        )

    with col2:

        priority_filter = st.selectbox(
            "Priority",
            ["All", "High", "Medium", "Low"]
        )

    with col3:

        status_filter = st.selectbox(
            "Status",
            ["All", "Pending", "Completed"]
        )


    # --------------------------------
    # Filter Tasks
    # --------------------------------

    filtered_tasks = []

    for task in tasks:

        task_id = task[0]
        subject = task[1]
        topic = task[2]
        priority = task[3]
        planned_date = task[4]
        duration = task[5]
        deadline = task[6]
        status = task[7]

        # Search filter
        search_match = (
            search_text.lower() in subject.lower()
            or
            search_text.lower() in topic.lower()
        )

        # Priority filter
        priority_match = (
            priority_filter == "All"
            or priority == priority_filter
        )

        # Status filter
        status_match = (
            status_filter == "All"
            or status == status_filter
        )

        if (
            search_match
            and priority_match
            and status_match
        ):

            filtered_tasks.append(task)


    # --------------------------------
    # Display Filter Result
    # --------------------------------

    st.write(
        f"Showing **{len(filtered_tasks)}** task(s)"
    )


    if not filtered_tasks:

        st.info(
            "🔎 No tasks match your filters."
        )


    # --------------------------------
    # Display Tasks
    # --------------------------------

    for task in filtered_tasks:

        task_id = task[0]
        subject = task[1]
        topic = task[2]
        priority = task[3]
        planned_date = task[4]
        duration = task[5]
        deadline = task[6]
        status = task[7]

        deadline_date = date.fromisoformat(
            deadline
        )

        is_overdue = (
            deadline_date < date.today()
            and status == "Pending"
        )


        # --------------------------------
        # Task Card
        # --------------------------------

        with st.container(border=True):

            if status == "Completed":

                st.markdown(
                    f"### ✅ {topic}"
                )

            elif is_overdue:

                st.markdown(
                    f"### ⚠️ {topic}"
                )

            else:

                st.markdown(
                    f"### 📚 {topic}"
                )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.write(
                    f"**Subject:** {subject}"
                )

                st.write(
                    f"**Priority:** {priority}"
                )


            with col2:

                st.write(
                    f"**Planned Date:** {planned_date}"
                )

                st.write(
                    f"**Duration:** {duration} minutes"
                )


            with col3:

                st.write(
                    f"**Deadline:** {deadline}"
                )

                st.write(
                    f"**Status:** {status}"
                )


            # --------------------------------
            # Task Status
            # --------------------------------

            if is_overdue:

                st.error(
                    "⚠️ This task is overdue!"
                )


            if status == "Pending":

                if st.button(
                    "✅ Mark as Completed",
                    key=f"complete_{task_id}"
                ):

                    update_task_status(
                        task_id,
                        "Completed"
                    )

                    st.success(
                        "🎉 Task completed!"
                    )

                    st.rerun()

            else:

                st.success(
                    "🎉 Completed"
                )


# --------------------------------
# No Tasks
# --------------------------------

else:

    st.info(
        "📖 No tasks yet. "
        "Add your first study task above!"
    )