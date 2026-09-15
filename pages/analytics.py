import streamlit as st
import plotly.express as px

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
# Page Header
# --------------------------------

st.title("📈 Study Analytics")

st.caption(
    "Understand your study habits and track your productivity."
)


# --------------------------------
# Get Data
# --------------------------------

tasks = get_tasks()
sessions = get_study_sessions()

df = sessions_to_dataframe(sessions)


# --------------------------------
# Empty State
# --------------------------------

if df.empty:

    st.info(
        "📚 No study sessions recorded yet."
    )

    st.write(
        "Start a session using the **Study Timer** "
        "to begin seeing your analytics."
    )

    st.stop()


# --------------------------------
# Key Statistics
# --------------------------------

total_minutes = get_total_study_minutes(df)

total_hours = total_minutes / 60

completed_tasks = sum(
    1
    for task in tasks
    if task[7] == "Completed"
)

total_tasks = len(tasks)

average_session = (
    total_minutes / len(sessions)
)


st.subheader("📊 Overview")

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
        "⏳ Avg. Session",
        f"{average_session:.0f} min"
    )


with col4:

    st.metric(
        "✅ Tasks Completed",
        f"{completed_tasks}/{total_tasks}"
    )


# --------------------------------
# Subject Analysis
# --------------------------------

st.divider()

st.subheader("📚 Study Time by Subject")

subject_summary = get_subject_summary(df)


chart_col1, chart_col2 = st.columns(2)


with chart_col1:

    fig_subject = px.pie(
        subject_summary,
        names="subject",
        values="duration_minutes",
        hole=0.45,
        title="Study Distribution"
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


with chart_col2:

    fig_subject_bar = px.bar(
        subject_summary,
        x="subject",
        y="duration_minutes",
        title="Study Minutes by Subject",
        labels={
            "subject": "Subject",
            "duration_minutes": "Minutes"
        }
    )

    fig_subject_bar.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig_subject_bar,
        use_container_width=True
    )


# --------------------------------
# Daily Study Trend
# --------------------------------

st.divider()

st.subheader("📅 Daily Study Trend")

daily_summary = get_daily_summary(df)


fig_daily = px.line(
    daily_summary,
    x="date",
    y="duration_minutes",
    markers=True,
    title="Study Time Over Days",
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
# Session History
# --------------------------------

st.divider()

st.subheader("📋 Study Session History")

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
    use_container_width=True,
    hide_index=True
)


# --------------------------------
# Study Insights
# --------------------------------

st.divider()

st.subheader("💡 Study Insights")


most_studied = subject_summary.iloc[0]

longest_session = df.loc[
    df["duration_minutes"].idxmax()
]


insight_col1, insight_col2 = st.columns(2)


with insight_col1:

    st.info(
        f"📚 **Most Studied Subject**\n\n"
        f"{most_studied['subject']} — "
        f"{most_studied['duration_minutes']} minutes"
    )


with insight_col2:

    st.info(
        f"⏱️ **Longest Session**\n\n"
        f"{longest_session['topic']} — "
        f"{longest_session['duration_minutes']} minutes"
    )


# --------------------------------
# Productivity Message
# --------------------------------

if average_session >= 45:

    st.success(
        "🌟 Your average study session is strong. "
        "Keep maintaining focused study sessions!"
    )

elif average_session >= 25:

    st.warning(
        "👍 Your study sessions are on a good track. "
        "Try gradually increasing focused study time."
    )

else:

    st.info(
        "💪 Try extending your focused study sessions "
        "to improve your overall study time."
    )