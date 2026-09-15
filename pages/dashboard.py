import streamlit as st
import plotly.express as px
from datetime import date, timedelta

from database.database import (
    create_table,
    get_tasks,
    get_study_sessions
)

from utils.analytics_utils import (
    sessions_to_dataframe,
    get_total_study_minutes,
    get_subject_summary,
    get_daily_summary
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="StudyFlow Dashboard",
    page_icon="📊",
    layout="wide"
)

create_table()


# =========================================================
# PAGE TITLE
# =========================================================

st.title("📊 StudyFlow Dashboard")

st.caption(
    "Your study progress at a glance. "
    "Plan better, study consistently, and keep improving."
)

st.divider()


# =========================================================
# LOAD DATA
# =========================================================

tasks = get_tasks()

sessions = get_study_sessions()

df = sessions_to_dataframe(sessions)


# =========================================================
# CALCULATE STATISTICS
# =========================================================

total_minutes = get_total_study_minutes(df)

total_hours = total_minutes / 60

total_sessions = len(sessions)

total_tasks = len(tasks)

completed_tasks = sum(
    1
    for task in tasks
    if task[7] == "Completed"
)

pending_tasks = (
    total_tasks - completed_tasks
)


# =========================================================
# TODAY'S STUDY
# =========================================================

today = date.today()

if not df.empty:

    today_df = df[
        df["date"] == today
    ]

    today_minutes = today_df[
        "duration_minutes"
    ].sum()

else:

    today_minutes = 0


today_hours = today_minutes / 60


# =========================================================
# DAILY STUDY GOAL
# =========================================================

st.subheader("🎯 Today's Study Goal")

st.caption(
    "Set a daily target and track your progress."
)

col1, col2 = st.columns(
    [3, 1]
)

with col1:

    if "daily_goal" not in st.session_state:

        st.session_state.daily_goal = 2.0

    daily_goal = st.slider(
        "Daily study goal (hours)",
        min_value=0.5,
        max_value=12.0,
        value=float(
            st.session_state.daily_goal
        ),
        step=0.5
    )

    st.session_state.daily_goal = daily_goal

with col2:

    st.metric(
        "Today's Study",
        f"{today_hours:.1f} h"
    )


goal_progress = min(
    today_hours / daily_goal,
    1.0
)

st.progress(
    goal_progress
)


if today_hours >= daily_goal:

    st.success(
        "🎉 Daily study goal achieved! "
        "Excellent work!"
    )

else:

    remaining = daily_goal - today_hours

    st.info(
        f"📚 {remaining:.1f} more hour(s) "
        "to reach today's goal."
    )


st.divider()


# =========================================================
# STUDY OVERVIEW
# =========================================================

st.subheader("📌 Study Overview")

st.caption(
    "Your overall StudyFlow activity."
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "⏱️ Total Study",
        f"{total_hours:.1f} h"
    )


with col2:

    st.metric(
        "📚 Sessions",
        total_sessions
    )


with col3:

    st.metric(
        "✅ Completed Tasks",
        completed_tasks
    )


with col4:

    st.metric(
        "⏳ Pending Tasks",
        pending_tasks
    )


st.divider()


# =========================================================
# STUDY STREAK
# =========================================================

st.subheader("🔥 Study Streak")

st.caption(
    "Your current consecutive study streak."
)


if df.empty:

    streak = 0

else:

    study_dates = set(
        df["date"]
    )

    streak = 0

    current_date = today

    while current_date in study_dates:

        streak += 1

        current_date = (
            current_date
            -
            timedelta(days=1)
        )


col1, col2 = st.columns(
    [1, 3]
)

with col1:

    st.metric(
        "🔥 Current Streak",
        f"{streak} day"
        if streak == 1
        else f"{streak} days"
    )

with col2:

    if streak == 0:

        st.info(
            "🚀 Start a study session today "
            "to begin your streak!"
        )

    elif streak == 1:

        st.info(
            "🔥 Great start! Study tomorrow "
            "to continue your streak."
        )

    else:

        st.success(
            f"🔥 Amazing! You've studied for "
            f"{streak} consecutive days."
        )


st.divider()


# =========================================================
# QUICK ACTIONS
# =========================================================

st.subheader("🚀 Quick Actions")

st.caption(
    "Your StudyFlow workflow."
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    with st.container(border=True):

        st.markdown("### 📝 Plan")

        st.caption(
            "Create tasks and organize "
            "your study schedule."
        )


with col2:

    with st.container(border=True):

        st.markdown("### ⏱️ Focus")

        st.caption(
            "Start a focused study session "
            "and track your time."
        )


with col3:

    with st.container(border=True):

        st.markdown("### 📈 Analyze")

        st.caption(
            "Understand your study patterns "
            "with charts."
        )


with col4:

    with st.container(border=True):

        st.markdown("### 🤖 Improve")

        st.caption(
            "Use ML predictions and "
            "recommendations."
        )


# =========================================================
# PRODUCTIVITY PREVIEW
# =========================================================

if not df.empty:

    st.divider()

    st.subheader("📈 Productivity Preview")

    st.caption(
        "A quick look at your recent study activity."
    )


    chart_col1, chart_col2 = st.columns(2)


    # -----------------------------------------------------
    # SUBJECT DISTRIBUTION
    # -----------------------------------------------------

    with chart_col1:

        subject_summary = get_subject_summary(
            df
        )

        fig_subject = px.pie(
            subject_summary,
            names="subject",
            values="duration_minutes",
            hole=0.5,
            title="Study Time by Subject"
        )

        fig_subject.update_layout(
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig_subject,
            use_container_width=True
        )


    # -----------------------------------------------------
    # DAILY TREND
    # -----------------------------------------------------

    with chart_col2:

        daily_summary = get_daily_summary(
            df
        )

        fig_daily = px.line(
            daily_summary,
            x="date",
            y="duration_minutes",
            markers=True,
            title="Daily Study Trend",
            labels={
                "date": "Date",
                "duration_minutes": "Study Minutes"
            }
        )

        fig_daily.update_layout(
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        st.plotly_chart(
            fig_daily,
            use_container_width=True
        )


# =========================================================
# TASK PROGRESS
# =========================================================

st.divider()

st.subheader("📝 Task Progress")

st.caption(
    "See how much of your study plan is complete."
)


if total_tasks == 0:

    st.info(
        "No tasks added yet. "
        "Go to Planner to create your first task."
    )

else:

    completion_percentage = (
        completed_tasks
        /
        total_tasks
    ) * 100


    st.progress(
        completion_percentage / 100
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Tasks Completed",
            f"{completed_tasks}/{total_tasks}"
        )


    with col2:

        st.metric(
            "Completion Rate",
            f"{completion_percentage:.1f}%"
        )


# =========================================================
# RECENT TASKS
# =========================================================

st.divider()

st.subheader("📋 Recent Tasks")

st.caption(
    "Your latest planned study tasks."
)


if tasks:

    for task in tasks[:5]:

        subject = task[1]

        topic = task[2]

        priority = task[3]

        status = task[7]


        if status == "Completed":

            icon = "✅"

        else:

            icon = "⏳"


        with st.container(border=True):

            col1, col2 = st.columns(
                [3, 1]
            )


            with col1:

                st.markdown(
                    f"### {icon} {topic}"
                )

                st.caption(
                    f"📚 {subject}"
                )


            with col2:

                if priority == "High":

                    st.error(
                        "🔴 High Priority"
                    )

                elif priority == "Medium":

                    st.warning(
                        "🟡 Medium Priority"
                    )

                else:

                    st.success(
                        "🟢 Low Priority"
                    )


else:

    st.info(
        "📝 No tasks yet. "
        "Create your first task in Planner."
    )


# =========================================================
# EMPTY PROJECT MESSAGE
# =========================================================

if df.empty and not tasks:

    st.divider()

    st.info(
        "🌱 Your StudyFlow journey starts here! "
        "Add a task in Planner and start your "
        "first study session using the Timer."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "📚 StudyFlow • Plan • Study • Analyze • Improve"
)