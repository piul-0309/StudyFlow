import streamlit as st
import plotly.express as px

from database.database import (
    create_table,
    get_study_sessions,
    get_tasks
)

from utils.analytics_utils import (
    sessions_to_dataframe,
    get_total_study_minutes,
    get_subject_summary,
    get_daily_summary
)


# Create database tables
create_table()


st.title("📊 Study Analytics")

st.write(
    "Understand your study habits and track your productivity."
)


# -----------------------------
# Load Data
# -----------------------------

sessions = get_study_sessions()

df = sessions_to_dataframe(sessions)


# -----------------------------
# Key Metrics
# -----------------------------

total_minutes = get_total_study_minutes(df)

total_hours = total_minutes / 60


tasks = get_tasks()

completed_tasks = sum(
    1 for task in tasks
    if task[7] == "Completed"
)


total_tasks = len(tasks)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "⏱️ Total Study Hours",
        f"{total_hours:.1f}"
    )


with col2:

    st.metric(
        "📚 Study Sessions",
        len(sessions)
    )


with col3:

    st.metric(
        "✅ Completed Tasks",
        completed_tasks
    )


with col4:

    st.metric(
        "📋 Total Tasks",
        total_tasks
    )


st.divider()


# -----------------------------
# No Data Message
# -----------------------------

if df.empty:

    st.info(
        "No study sessions recorded yet. "
        "Complete a session using the Timer to see your analytics! 📈"
    )

else:

    # -----------------------------
    # Subject-wise Study Time
    # -----------------------------

    st.subheader("📚 Study Time by Subject")

    subject_summary = get_subject_summary(df)

    fig_subject = px.bar(
        subject_summary,
        x="subject",
        y="duration_minutes",
        title="Study Minutes by Subject",
        labels={
            "subject": "Subject",
            "duration_minutes": "Study Minutes"
        }
    )

    st.plotly_chart(
        fig_subject,
        use_container_width=True
    )


    # -----------------------------
    # Daily Study Trend
    # -----------------------------

    st.subheader("📈 Daily Study Trend")

    daily_summary = get_daily_summary(df)

    fig_daily = px.line(
        daily_summary,
        x="date",
        y="duration_minutes",
        markers=True,
        title="Study Time Over Time",
        labels={
            "date": "Date",
            "duration_minutes": "Study Minutes"
        }
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )


    # -----------------------------
    # Study Sessions
    # -----------------------------

    st.subheader("🕐 Study Session History")

    display_df = df[
        [
            "subject",
            "topic",
            "start_time",
            "end_time",
            "duration_minutes"
        ]
    ].copy()

    display_df.columns = [
        "Subject",
        "Topic",
        "Start Time",
        "End Time",
        "Duration (minutes)"
    ]

    st.dataframe(
        display_df,
        use_container_width=True
    )