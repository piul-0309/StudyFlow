import streamlit as st
from datetime import date

from database.database import (
    create_table,
    add_task,
    get_tasks,
    update_task_status
)


# --------------------------------
# Database
# --------------------------------

create_table()


# --------------------------------
# Page Header
# --------------------------------

st.title("📝 Study Planner")

st.caption(
    "Organize your study tasks, priorities, and deadlines."
)


# --------------------------------
# Add Task Section
# --------------------------------

st.subheader("➕ Add a New Study Task")

with st.container(border=True):

    with st.form("task_form"):

        col1, col2 = st.columns(2)

        with col1:

            subject = st.text_input(
                "📚 Subject",
                placeholder="e.g. Data Structures"
            )

            topic = st.text_input(
                "📖 Topic / Task",
                placeholder="e.g. Binary Search"
            )

            priority = st.selectbox(
                "🎯 Priority",
                ["High", "Medium", "Low"]
            )

        with col2:

            planned_date = st.date_input(
                "📅 Planned Date",
                date.today()
            )

            deadline = st.date_input(
                "⏰ Deadline",
                date.today()
            )

            planned_duration = st.number_input(
                "⏱️ Planned Duration (minutes)",
                min_value=15,
                max_value=600,
                value=60,
                step=15
            )

        submitted = st.form_submit_button(
            "➕ Add Study Task",
            use_container_width=True
        )


        # --------------------------------
        # Add Task
        # --------------------------------

        if submitted:

            if not subject:

                st.error(
                    "Please enter a subject."
                )

            elif not topic:

                st.error(
                    "Please enter a topic or task."
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
                    f"🎉 '{topic}' added successfully!"
                )

                st.rerun()


# --------------------------------
# Get Tasks
# --------------------------------

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

pending_tasks = (
    total_tasks
    -
    completed_tasks
)

overdue_tasks = 0

for task in tasks:

    deadline = date.fromisoformat(
        task[6]
    )

    status = task[7]

    if (
        deadline < date.today()
        and status == "Pending"
    ):

        overdue_tasks += 1


# --------------------------------
# Statistics
# --------------------------------

st.divider()

st.subheader("📊 Task Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📚 Total",
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
# Progress
# --------------------------------

if total_tasks > 0:

    completion_percentage = (
        completed_tasks
        /
        total_tasks
    ) * 100

    st.write(
        f"**Overall Progress — "
        f"{completion_percentage:.0f}%**"
    )

    st.progress(
        completion_percentage / 100
    )


# --------------------------------
# Filters
# --------------------------------

if tasks:

    st.divider()

    st.subheader("🔎 Find Your Tasks")

    col1, col2, col3 = st.columns(3)

    with col1:

        search_text = st.text_input(
            "Search",
            placeholder="Subject or topic..."
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

        subject = task[1]
        topic = task[2]
        priority = task[3]
        status = task[7]

        search_match = (
            search_text.lower()
            in subject.lower()
            or
            search_text.lower()
            in topic.lower()
        )

        priority_match = (
            priority_filter == "All"
            or
            priority == priority_filter
        )

        status_match = (
            status_filter == "All"
            or
            status == status_filter
        )

        if (
            search_match
            and priority_match
            and status_match
        ):

            filtered_tasks.append(task)


    st.caption(
        f"{len(filtered_tasks)} task(s) found"
    )


    # --------------------------------
    # Display Tasks
    # --------------------------------

    if not filtered_tasks:

        st.info(
            "🔎 No tasks match your filters."
        )


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
                    f"**Subject**  \n{subject}"
                )

                st.write(
                    f"**Priority**  \n{priority}"
                )


            with col2:

                st.write(
                    f"**Planned Date**  \n{planned_date}"
                )

                st.write(
                    f"**Duration**  \n{duration} minutes"
                )


            with col3:

                st.write(
                    f"**Deadline**  \n{deadline}"
                )

                if status == "Completed":

                    st.success(
                        "Completed"
                    )

                elif is_overdue:

                    st.error(
                        "Overdue"
                    )

                else:

                    st.warning(
                        "Pending"
                    )


            # --------------------------------
            # Complete Button
            # --------------------------------

            if status == "Pending":

                if st.button(
                    "✅ Mark as Completed",
                    key=f"complete_{task_id}",
                    use_container_width=True
                ):

                    update_task_status(
                        task_id,
                        "Completed"
                    )

                    st.success(
                        "🎉 Task completed!"
                    )

                    st.rerun()


# --------------------------------
# Empty State
# --------------------------------

else:

    st.divider()

    st.info(
        "📖 No study tasks yet."
    )

    st.write(
        "Add your first task above to start planning your studies! 🚀"
    )