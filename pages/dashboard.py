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


# --------------------------------
# Create Database Tables
# --------------------------------

create_table()


# --------------------------------
# Page Title
# --------------------------------

st.title("📈 StudyFlow Dashboard")

st.write(
    "Your study progress and productivity at a glance."
)


# --------------------------------
# Daily Study Goal
# --------------------------------

st.subheader("🎯 Daily Study Goal")

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 2.0

daily_goal = st.number_input(
    "Set your daily study goal (hours)",
    min_value=0.5,
    max_value=12.0,
    value=st.session_state.daily_goal,
    step=0.5
)

st.session_state.daily_goal = daily_goal


# --------------------------------
# Load Data
# --------------------------------

tasks = get_tasks()
sessions = get_study_sessions()

df = sessions_to_dataframe(sessions)


# --------------------------------
# Study Statistics
# --------------------------------

total_minutes = get_total_study_minutes(df)

total_hours = total_minutes / 60

completed_tasks = sum(
    1
    for task in tasks
    if task[7] == "Completed"
)

total_tasks = len(tasks)

pending_tasks = total_tasks - completed_tasks


# --------------------------------
# Today's Study Time
# --------------------------------

today = date.today()

if not df.empty:

    today_df = df[df["date"] == today]

    today_minutes = today_df["duration_minutes"].sum()

else:

    today_minutes = 0


today_hours = today_minutes / 60

goal_progress = min(
    today_hours / daily_goal,
    1.0
)


# --------------------------------
# Dashboard Metrics
# --------------------------------

st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "⏱️ Study Hours",
        f"{total_hours:.1f}"
    )


with col2:

    st.metric(
        "📚 Sessions",
        len(sessions)
    )


with col3:

    st.metric(
        "✅ Completed",
        completed_tasks
    )


with col4:

    st.metric(
        "⏳ Pending",
        pending_tasks
    )


# --------------------------------
# Today's Goal
# --------------------------------

st.divider()

st.subheader("🎯 Today's Goal")

st.progress(goal_progress)

st.write(
    f"**{today_hours:.1f} / {daily_goal:.1f} hours completed**"
)


if today_hours >= daily_goal:

    st.success(
        "🎉 Daily study goal achieved! Amazing work!"
    )

else:

    remaining = daily_goal - today_hours

    st.info(
        f"📚 {remaining:.1f} more hour(s) "
        "to reach today's goal."
    )


# --------------------------------
# Study Streak
# --------------------------------

st.subheader("🔥 Study Streak")

if df.empty:

    streak = 0

else:

    study_dates = set(df["date"])

    streak = 0

    current_date = today

    while current_date in study_dates:

        streak += 1

        current_date = (
            current_date - timedelta(days=1)
        )


st.metric(
    "🔥 Current Study Streak",
    f"{streak} day(s)"
)


if streak == 0:

    st.write(
        "Start studying today to begin your streak! 🚀"
    )

elif streak == 1:

    st.write(
        "🔥 Great start! Come back tomorrow "
        "to make it a 2-day streak."
    )

else:

    st.success(
        f"🔥 Amazing! You've studied for "
        f"{streak} consecutive days!"
    )


# --------------------------------
# Study Analytics
# --------------------------------

if df.empty:

    st.divider()

    st.info(
        "Start a study session using the Timer "
        "to see your study analytics! 📚"
    )

else:

    # --------------------------------
    # Subject-wise Study Time
    # --------------------------------

    st.divider()

    st.subheader("📚 Study Time by Subject")

    subject_summary = get_subject_summary(df)

    fig_subject = px.pie(
        subject_summary,
        names="subject",
        values="duration_minutes",
        title="Where You're Spending Your Study Time"
    )

    st.plotly_chart(
        fig_subject,
        use_container_width=True
    )


    # --------------------------------
    # Daily Study Trend
    # --------------------------------

    st.subheader("📈 Study Trend")

    daily_summary = get_daily_summary(df)

    fig_daily = px.line(
        daily_summary,
        x="date",
        y="duration_minutes",
        markers=True,
        title="Daily Study Time",
        labels={
            "date": "Date",
            "duration_minutes": "Study Minutes"
        }
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )


# --------------------------------
# Task Progress
# --------------------------------

st.divider()

st.subheader("📝 Task Progress")


if total_tasks == 0:

    st.info(
        "No tasks added yet. "
        "Go to Planner to add your first task."
    )

else:

    completion_percentage = (
        completed_tasks / total_tasks
    ) * 100

    st.progress(
        completion_percentage / 100
    )

    st.write(
        f"**{completed_tasks} of {total_tasks} tasks completed "
        f"({completion_percentage:.1f}%)**"
    )


# --------------------------------
# Recent Tasks
# --------------------------------

st.subheader("📋 Recent Tasks")


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

        st.write(
            f"{icon} **{topic}** — "
            f"{subject} — {priority} priority"
        )

else:

    st.info(
        "No tasks available."
    )