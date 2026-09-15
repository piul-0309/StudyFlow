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


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StudyFlow Analytics",
    page_icon="📈",
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


/* =====================================================
   HERO
   ===================================================== */

.analytics-hero {
    padding: 1.8rem 2rem;
    border-radius: 22px;

    background: linear-gradient(
        135deg,
        #6C63FF,
        #8B83FF
    );

    color: white;

    margin-bottom: 1.8rem;

    box-shadow:
        0 12px 30px rgba(108, 99, 255, 0.22);
}


.analytics-title {
    font-size: 2rem;
    font-weight: 750;
}


.analytics-subtitle {
    font-size: 0.92rem;
    opacity: 0.9;
    margin-top: 0.25rem;
}


/* =====================================================
   SECTION
   ===================================================== */

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


/* =====================================================
   STAT CARDS
   ===================================================== */

.stat-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 18px;

    padding: 1.2rem;

    min-height: 125px;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.05);
}


.stat-icon {
    font-size: 1.35rem;
}


.stat-label {
    color: #6B7280;

    font-size: 0.75rem;

    font-weight: 700;

    margin-top: 0.35rem;
}


.stat-value {
    color: #111827;

    font-size: 1.7rem;

    font-weight: 750;

    margin-top: 0.15rem;
}


.stat-description {
    color: #9CA3AF;

    font-size: 0.75rem;

    margin-top: 0.2rem;
}


/* =====================================================
   INSIGHT CARDS
   ===================================================== */

.insight-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 18px;

    padding: 1.3rem;

    min-height: 125px;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.04);
}


.insight-title {
    color: #6B7280;

    font-size: 0.75rem;

    font-weight: 700;
}


.insight-value {
    color: #111827;

    font-size: 1.15rem;

    font-weight: 750;

    margin-top: 0.35rem;
}


.insight-text {
    color: #6B7280;

    font-size: 0.8rem;

    margin-top: 0.25rem;
}


/* =====================================================
   CHART CONTAINER
   ===================================================== */

.chart-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 18px;

    padding: 0.6rem;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.04);
}


/* =====================================================
   EMPTY STATE
   ===================================================== */

.empty-card {
    text-align: center;

    padding: 3rem 2rem;

    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 22px;

    box-shadow:
        0 6px 20px rgba(0, 0, 0, 0.04);
}


.empty-icon {
    font-size: 3rem;
}


.empty-title {
    color: #111827;

    font-size: 1.2rem;

    font-weight: 700;

    margin-top: 0.5rem;
}


.empty-text {
    color: #6B7280;

    font-size: 0.85rem;

    margin-top: 0.3rem;
}


/* =====================================================
   FOOTER
   ===================================================== */

.analytics-footer {
    text-align: center;

    margin-top: 2.5rem;

    padding-top: 1.2rem;

    border-top: 1px solid #E5E7EB;

    color: #9CA3AF;

    font-size: 0.75rem;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="analytics-hero">'
    '<div class="analytics-title">'
    '📈 Study Analytics'
    '</div>'
    '<div class="analytics-subtitle">'
    'Understand your study habits, discover patterns, '
    'and track your productivity over time.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

tasks = get_tasks()

sessions = get_study_sessions()

df = sessions_to_dataframe(sessions)


# =========================================================
# EMPTY STATE
# =========================================================

if df.empty:

    st.markdown(
        '<div class="empty-card">'
        '<div class="empty-icon">📊</div>'
        '<div class="empty-title">'
        'No study data yet'
        '</div>'
        '<div class="empty-text">'
        'Complete a study session using the Timer '
        'and your analytics will appear here.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# BASIC CALCULATIONS
# =========================================================

total_minutes = get_total_study_minutes(df)

total_hours = total_minutes / 60

total_sessions = len(sessions)

average_session = (
    total_minutes / total_sessions
)

completed_tasks = sum(
    1
    for task in tasks
    if task[7] == "Completed"
)

total_tasks = len(tasks)


if total_tasks > 0:

    completion_percentage = (
        completed_tasks / total_tasks
    ) * 100

else:

    completion_percentage = 0


# =========================================================
# OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📊 Your Overview'
    '</div>'
    '<div class="section-subtitle">'
    'Key statistics from your recorded study activity.'
    '</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-icon">⏱️</div>'
        '<div class="stat-label">TOTAL STUDY</div>'
        f'<div class="stat-value">'
        f'{total_hours:.1f} h'
        f'</div>'
        '<div class="stat-description">'
        'Across all sessions'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-icon">📚</div>'
        '<div class="stat-label">STUDY SESSIONS</div>'
        f'<div class="stat-value">'
        f'{total_sessions}'
        f'</div>'
        '<div class="stat-description">'
        'Sessions recorded'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-icon">⏳</div>'
        '<div class="stat-label">AVG. SESSION</div>'
        f'<div class="stat-value">'
        f'{average_session:.0f} min'
        f'</div>'
        '<div class="stat-description">'
        'Average focused time'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-icon">✅</div>'
        '<div class="stat-label">TASK COMPLETION</div>'
        f'<div class="stat-value">'
        f'{completion_percentage:.0f}%'
        f'</div>'
        '<div class="stat-description">'
        f'{completed_tasks} of {total_tasks} completed'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# SUBJECT ANALYSIS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📚 Subject Analysis'
    '</div>'
    '<div class="section-subtitle">'
    'See where your study time is being spent.'
    '</div>',
    unsafe_allow_html=True
)


subject_summary = get_subject_summary(df)


chart_col1, chart_col2 = st.columns(2)


# =========================================================
# PIE CHART
# =========================================================

with chart_col1:

    fig_subject = px.pie(
        subject_summary,

        names="subject",

        values="duration_minutes",

        hole=0.5,

        title="Study Time Distribution"
    )

    fig_subject.update_layout(
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        legend_title_text="Subject"
    )

    st.plotly_chart(
        fig_subject,
        use_container_width=True
    )


# =========================================================
# BAR CHART
# =========================================================

with chart_col2:

    fig_subject_bar = px.bar(
        subject_summary,

        x="subject",

        y="duration_minutes",

        title="Minutes Studied by Subject",

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


# =========================================================
# DAILY TREND
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📅 Daily Study Trend'
    '</div>'
    '<div class="section-subtitle">'
    'Track how your study time changes from day to day.'
    '</div>',
    unsafe_allow_html=True
)


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


# =========================================================
# STUDY INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '💡 Study Insights'
    '</div>'
    '<div class="section-subtitle">'
    'Simple observations from your study data.'
    '</div>',
    unsafe_allow_html=True
)


most_studied = subject_summary.iloc[0]

longest_session = df.loc[
    df["duration_minutes"].idxmax()
]


insight_col1, insight_col2 = st.columns(2)


with insight_col1:

    st.markdown(
        '<div class="insight-card">'
        '<div class="insight-title">'
        '📚 MOST STUDIED SUBJECT'
        '</div>'
        '<div class="insight-value">'
        f'{most_studied["subject"]}'
        '</div>'
        '<div class="insight-text">'
        f'{most_studied["duration_minutes"]} minutes studied'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


with insight_col2:

    st.markdown(
        '<div class="insight-card">'
        '<div class="insight-title">'
        '⏱️ LONGEST SESSION'
        '</div>'
        '<div class="insight-value">'
        f'{longest_session["topic"]}'
        '</div>'
        '<div class="insight-text">'
        f'{longest_session["duration_minutes"]} minutes'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# STUDY HABIT MESSAGE
# =========================================================

st.write("")


if average_session >= 45:

    st.success(
        "🌟 Your average study session is strong. "
        "Keep maintaining focused sessions!"
    )

elif average_session >= 25:

    st.info(
        "👍 Your study sessions are on a good track. "
        "Try gradually increasing your focused study time."
    )

else:

    st.warning(
        "💪 Your sessions are currently short. "
        "Try gradually extending your focused study time."
    )


# =========================================================
# SESSION HISTORY
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📋 Session History'
    '</div>'
    '<div class="section-subtitle">'
    'Review all of your recorded study sessions.'
    '</div>',
    unsafe_allow_html=True
)


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


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="analytics-footer">'
    '📈 StudyFlow Analytics &nbsp;•&nbsp; '
    'Measure &nbsp;•&nbsp; Understand &nbsp;•&nbsp; Improve'
    '</div>',
    unsafe_allow_html=True
)