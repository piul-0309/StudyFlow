import streamlit as st


# --------------------------------
# Page Configuration
# --------------------------------

st.set_page_config(
    page_title="StudyFlow",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------
# Header
# --------------------------------

st.title("📚 StudyFlow")

st.subheader(
    "Your Smart Study Planner & Productivity Assistant"
)

st.write(
    "Plan your studies, track your study time, "
    "analyze your productivity, and use machine learning "
    "to understand your performance."
)


# --------------------------------
# Quick Overview
# --------------------------------

st.divider()

st.subheader("🚀 What can you do with StudyFlow?")


col1, col2, col3 = st.columns(3)


with col1:

    st.markdown("### 📝 Plan")

    st.write(
        "Create study tasks, set priorities, "
        "deadlines, and planned study durations."
    )


with col2:

    st.markdown("### ⏱️ Track")

    st.write(
        "Use the study timer to record your "
        "actual study sessions automatically."
    )


with col3:

    st.markdown("### 🤖 Improve")

    st.write(
        "Analyze your study habits and get "
        "ML-based performance predictions."
    )


# --------------------------------
# Features
# --------------------------------

st.divider()

st.subheader("✨ StudyFlow Features")


features = [
    "📝 **Study Planner** — Organize subjects, topics, priorities and deadlines.",
    "⏱️ **Study Timer** — Record your actual study sessions.",
    "📈 **Analytics Dashboard** — Understand your study patterns.",
    "🔥 **Study Streaks** — Stay consistent with your study routine.",
    "🎯 **Daily Goals** — Set and track your daily study target.",
    "🤖 **ML Predictions** — Predict performance using study habits.",
    "💡 **Smart Recommendations** — Get personalized suggestions.",
    "🗄️ **SQLite Database** — Store tasks and study sessions locally."
]


for feature in features:

    st.write(feature)


# --------------------------------
# How StudyFlow Works
# --------------------------------

st.divider()

st.subheader("🔄 How StudyFlow Works")


step1, step2, step3, step4 = st.columns(4)


with step1:

    st.markdown("### 1️⃣ Plan")

    st.write(
        "Add your study tasks and deadlines."
    )


with step2:

    st.markdown("### 2️⃣ Study")

    st.write(
        "Start the timer and focus on your task."
    )


with step3:

    st.markdown("### 3️⃣ Analyze")

    st.write(
        "View your study hours, trends and progress."
    )


with step4:

    st.markdown("### 4️⃣ Improve")

    st.write(
        "Use ML predictions and recommendations "
        "to improve your study habits."
    )


# --------------------------------
# Tech Stack
# --------------------------------

st.divider()

st.subheader("🛠️ Technology Stack")


tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)


with tech_col1:

    st.markdown("**🐍 Python**")

    st.caption(
        "Core programming language"
    )


with tech_col2:

    st.markdown("**🎈 Streamlit**")

    st.caption(
        "Web application framework"
    )


with tech_col3:

    st.markdown("**📊 Pandas & Plotly**")

    st.caption(
        "Data analysis and visualization"
    )


with tech_col4:

    st.markdown("**🤖 Scikit-learn**")

    st.caption(
        "Machine learning"
    )


# --------------------------------
# Getting Started
# --------------------------------

st.divider()

st.subheader("🎯 Getting Started")

st.info(
    "👈 Use the sidebar to open **Study Planner**, "
    "**Study Timer**, **Analytics**, or "
    "**AI Performance Prediction**."
)


# --------------------------------
# Footer
# --------------------------------

st.divider()

st.caption(
    "📚 StudyFlow — Plan • Study • Analyze • Improve"
)