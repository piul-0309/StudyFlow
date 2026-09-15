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
# Database
# --------------------------------

create_table()


# --------------------------------
# Page Configuration
# --------------------------------

st.title("📊 Dashboard")

st.caption(
    "A quick overview of your study progress and productivity."
)


# --------------------------------
# Get Data
# --------------------------------

tasks = get_tasks()
sessions = get_study_sessions()

df = sessions_to_dataframe(sessions)


# --------------------------------
# Calculate Statistics
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

    today_minutes = today_df[
        "duration_minutes"
    ].sum()

else:

    today_minutes = 0


today_hours = today_minutes / 60


# --------------------------------
# Daily Goal
# --------------------------------

if "daily_goal" not in st.session_state:

    st.session_state.daily_goal = 2.0


st.subheader("🎯 Today's Goal")


goal_col1, goal_col2 = st.columns([3, 1])


with goal_col1:

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


with goal_col2:

    st.metric(
        "Today's Study",
        f"{today_hours:.1f} h"
    )


goal_progress = min(
    today_hours / daily_goal,
    1.0
)


st.progress(goal_progress)


if today_hours >= daily_goal:

    st.success(
        "🎉 Daily study goal achieved! Keep it up!"
    )

else:

    remaining = daily_goal - today_hours

    st.info(
        f"📚 You need {remaining:.1f} more hour(s) "
        "to reach today's goal."
    )


# --------------------------------
# Main Statistics
# --------------------------------

st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "⏱️ Total Study",
        f"{total_hours:.1f} h"
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
# Study Streak
# --------------------------------

st.divider()

st.subheader("🔥 Study Streak")


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


st.metric(
    "Current Streak",
    f"{streak} day(s)"
)


if streak == 0:

    st.write(
        "🚀 Start studying today to begin your streak!"
    )

elif streak == 1:

    st.write(
        "🔥 Great start! Study tomorrow to continue your streak."
    )

else:

    st.success(
        f"🔥 Amazing! You've studied for "
        f"{streak} consecutive days."
    )


# --------------------------------
# Charts
# --------------------------------

if not df.empty:

    st.divider()

    st.subheader("📈 Your Study Analytics")


    chart_col1, chart_col2 = st.columns(2)


    # --------------------------------
    # Subject Chart
    # --------------------------------

    with chart_col1:

        subject_summary = get_subject_summary(
            df
        )

        fig_subject = px.pie(
            subject_summary,
            names="subject",
            values="duration_minutes",
            hole=0.45,
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


    # --------------------------------
    # Daily Trend
    # --------------------------------

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


# --------------------------------
# Task Progress
# --------------------------------

st.divider()

st.subheader("📝 Task Progress")


if total_tasks == 0:

    st.info(
        "No tasks added yet. "
        "Go to the Planner to add your first task."
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


# --------------------------------
# Recent Tasks
# --------------------------------

st.divider()

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
            f"{icon} **{topic}**  •  "
            f"{subject}  •  "
            f"{priority} priority"
        )

else:

    st.info(
        "No tasks available."
    )


# --------------------------------
# Empty State
# --------------------------------

if df.empty and not tasks:

    st.divider()

    st.info(
        "🌱 Your StudyFlow journey starts here! "
        "Add a task in Planner and start a session "
        "using the Timer."
    )