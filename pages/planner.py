import streamlit as st
from datetime import date

from database.database import (
    create_table,
    add_task,
    get_tasks,
    update_task_status
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StudyFlow Planner",
    page_icon="📝",
    layout="wide"
)

create_table()


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* HERO */

.planner-hero {
    padding: 1.8rem 2rem;
    border-radius: 22px;
    background: linear-gradient(135deg, #6C63FF, #8B83FF);
    color: white;
    margin-bottom: 1.7rem;
    box-shadow: 0 12px 30px rgba(108, 99, 255, 0.22);
}

.planner-title {
    font-size: 2rem;
    font-weight: 750;
}

.planner-subtitle {
    font-size: 0.95rem;
    opacity: 0.9;
    margin-top: 0.25rem;
}

/* SECTION */

.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.15rem;
}

.section-subtitle {
    font-size: 0.85rem;
    opacity: 0.65;
    margin-bottom: 1rem;
}

/* FORM CARD */

.form-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}

/* STAT CARDS */

.stat-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 17px;
    padding: 1.15rem;
    min-height: 115px;
    box-shadow: 0 5px 16px rgba(0, 0, 0, 0.05);
}

.stat-icon {
    font-size: 1.35rem;
}

.stat-label {
    color: #6B7280;
    font-size: 0.76rem;
    font-weight: 700;
    margin-top: 0.35rem;
}

.stat-value {
    color: #111827;
    font-size: 1.7rem;
    font-weight: 750;
    margin-top: 0.15rem;
}

/* TASK CARD */

.task-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 5px 16px rgba(0, 0, 0, 0.04);
}

.task-card-completed {
    background: #F8FAFC;
    border: 1px solid #D1FAE5;
}

.task-card-overdue {
    border: 1px solid #FECACA;
    background: #FFF7F7;
}

.task-title {
    color: #111827;
    font-size: 1.05rem;
    font-weight: 700;
}

.task-subject {
    color: #6B7280;
    font-size: 0.82rem;
    margin-top: 0.2rem;
}

.task-meta {
    color: #6B7280;
    font-size: 0.78rem;
    margin-top: 0.65rem;
}

.priority-high {
    color: #DC2626;
    font-weight: 700;
}

.priority-medium {
    color: #D97706;
    font-weight: 700;
}

.priority-low {
    color: #16A34A;
    font-weight: 700;
}

.status-completed {
    color: #16A34A;
    font-weight: 700;
}

.status-pending {
    color: #D97706;
    font-weight: 700;
}

.status-overdue {
    color: #DC2626;
    font-weight: 700;
}

/* PROGRESS */

.progress-label {
    color: #6B7280;
    font-size: 0.8rem;
    margin-bottom: 0.35rem;
}

/* EMPTY */

.empty-card {
    text-align: center;
    padding: 2.5rem;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    margin-top: 1rem;
}

.empty-icon {
    font-size: 2.8rem;
}

.empty-title {
    color: #111827;
    font-size: 1.15rem;
    font-weight: 700;
    margin-top: 0.6rem;
}

.empty-text {
    color: #6B7280;
    font-size: 0.85rem;
    margin-top: 0.35rem;
}

/* BUTTON */

.stButton > button {
    border-radius: 12px;
    min-height: 42px;
    font-weight: 600;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="planner-hero">'
    '<div class="planner-title">📝 Study Planner</div>'
    '<div class="planner-subtitle">'
    'Turn your study goals into organized tasks and stay on track.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# ADD TASK
# =========================================================

st.markdown(
    '<div class="section-title">➕ Create a Study Task</div>'
    '<div class="section-subtitle">'
    'Plan what you want to study and when you want to complete it.'
    '</div>',
    unsafe_allow_html=True
)


with st.container(border=True):

    with st.form("task_form"):

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # LEFT
        # -------------------------------------------------

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

        # -------------------------------------------------
        # RIGHT
        # -------------------------------------------------

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

        st.write("")

        submitted = st.form_submit_button(
            "➕ Add Study Task",
            use_container_width=True
        )

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


# =========================================================
# LOAD TASKS
# =========================================================

tasks = get_tasks()

total_tasks = len(tasks)

completed_tasks = sum(
    1
    for task in tasks
    if task[7] == "Completed"
)

pending_tasks = total_tasks - completed_tasks

overdue_tasks = 0

for task in tasks:

    deadline_date = date.fromisoformat(
        task[6]
    )

    status = task[7]

    if (
        deadline_date < date.today()
        and status == "Pending"
    ):
        overdue_tasks += 1


# =========================================================
# TASK OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📊 Task Overview</div>'
    '<div class="section-subtitle">'
    'A quick summary of your current study workload.'
    '</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-icon">📚</div>'
        '<div class="stat-label">TOTAL TASKS</div>'
        f'<div class="stat-value">{total_tasks}</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-icon">⏳</div>'
        '<div class="stat-label">PENDING</div>'
        f'<div class="stat-value">{pending_tasks}</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-icon">✅</div>'
        '<div class="stat-label">COMPLETED</div>'
        f'<div class="stat-value">{completed_tasks}</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-icon">⚠️</div>'
        '<div class="stat-label">OVERDUE</div>'
        f'<div class="stat-value">{overdue_tasks}</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# OVERALL PROGRESS
# =========================================================

if total_tasks > 0:

    completion_percentage = (
        completed_tasks / total_tasks
    ) * 100

    st.write("")

    st.markdown(
        f'<div class="progress-label">'
        f'<strong>Overall Progress</strong>'
        f' &nbsp; {completion_percentage:.0f}%'
        f'</div>',
        unsafe_allow_html=True
    )

    st.progress(
        completion_percentage / 100
    )


# =========================================================
# SEARCH & FILTER
# =========================================================

if tasks:

    st.markdown(
        '<div class="section-title">🔎 Find Your Tasks</div>'
        '<div class="section-subtitle">'
        'Search and filter your study plan.'
        '</div>',
        unsafe_allow_html=True
    )

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


    # -----------------------------------------------------
    # FILTER TASKS
    # -----------------------------------------------------

    filtered_tasks = []

    for task in tasks:

        subject = task[1]
        topic = task[2]
        priority = task[3]
        status = task[7]

        search_match = (
            search_text.lower() in subject.lower()
            or
            search_text.lower() in topic.lower()
        )

        priority_match = (
            priority_filter == "All"
            or priority == priority_filter
        )

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


    st.caption(
        f"{len(filtered_tasks)} task(s) found"
    )


    # =====================================================
    # NO FILTER RESULTS
    # =====================================================

    if not filtered_tasks:

        st.info(
            "🔎 No tasks match your current filters."
        )


    # =====================================================
    # DISPLAY TASKS
    # =====================================================

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


        # -------------------------------------------------
        # CARD STYLE
        # -------------------------------------------------

        if status == "Completed":

            card_class = "task-card task-card-completed"

            icon = "✅"

            status_html = (
                '<span class="status-completed">'
                'Completed'
                '</span>'
            )

        elif is_overdue:

            card_class = "task-card task-card-overdue"

            icon = "⚠️"

            status_html = (
                '<span class="status-overdue">'
                'Overdue'
                '</span>'
            )

        else:

            card_class = "task-card"

            icon = "📚"

            status_html = (
                '<span class="status-pending">'
                'Pending'
                '</span>'
            )


        # -------------------------------------------------
        # PRIORITY STYLE
        # -------------------------------------------------

        if priority == "High":

            priority_html = (
                '<span class="priority-high">'
                'High'
                '</span>'
            )

        elif priority == "Medium":

            priority_html = (
                '<span class="priority-medium">'
                'Medium'
                '</span>'
            )

        else:

            priority_html = (
                '<span class="priority-low">'
                'Low'
                '</span>'
            )


        # -------------------------------------------------
        # TASK CARD
        # -------------------------------------------------

        st.markdown(
            f'<div class="{card_class}">'
            f'<div class="task-title">'
            f'{icon} {topic}'
            f'</div>'
            f'<div class="task-subject">'
            f'📚 {subject}'
            f'</div>'
            f'<div class="task-meta">'
            f'🎯 Priority: {priority_html}'
            f'&nbsp;&nbsp;•&nbsp;&nbsp;'
            f'⏱️ {duration} min'
            f'&nbsp;&nbsp;•&nbsp;&nbsp;'
            f'📅 Planned: {planned_date}'
            f'&nbsp;&nbsp;•&nbsp;&nbsp;'
            f'⏰ Deadline: {deadline}'
            f'&nbsp;&nbsp;•&nbsp;&nbsp;'
            f'{status_html}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )


        # -------------------------------------------------
        # COMPLETE BUTTON
        # -------------------------------------------------

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


# =========================================================
# EMPTY STATE
# =========================================================

else:

    st.markdown(
        '<div class="empty-card">'
        '<div class="empty-icon">📖</div>'
        '<div class="empty-title">'
        'Your study plan is empty'
        '</div>'
        '<div class="empty-text">'
        'Create your first study task above '
        'and start organizing your learning journey.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div style="'
    'text-align:center;'
    'margin-top:2.5rem;'
    'padding-top:1.2rem;'
    'border-top:1px solid #E5E7EB;'
    'color:#9CA3AF;'
    'font-size:0.75rem;">'
    '📚 StudyFlow &nbsp;•&nbsp; '
    'Plan your work &nbsp;•&nbsp; '
    'Track your progress'
    '</div>',
    unsafe_allow_html=True
)