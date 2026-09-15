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
# Hero Section
# --------------------------------

st.title("📚 StudyFlow")

st.subheader(
    "Your Smart Study Planner & Productivity Assistant"
)

st.write(
    "Plan your studies, track your study time, "
    "understand your productivity, and use machine learning "
    "to improve your study habits."
)


# --------------------------------
# Quick Navigation
# --------------------------------

st.divider()

st.subheader("🚀 Explore StudyFlow")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown("### 📝 Planner")

    st.caption(
        "Create tasks, set priorities, and manage deadlines."
    )


with col2:

    st.markdown("### ⏱️ Timer")

    st.caption(
        "Focus on your studies and record your sessions."
    )


with col3:

    st.markdown("### 📈 Analytics")

    st.caption(
        "Understand your study patterns and progress."
    )


with col4:

    st.markdown("### 🤖 AI Prediction")

    st.caption(
        "Predict performance and get smart recommendations."
    )


# --------------------------------
# Main Workflow
# --------------------------------

st.divider()

st.subheader("🔄 How StudyFlow Works")


step1, step2, step3, step4 = st.columns(4)


with step1:

    st.markdown("### 1️⃣ Plan")

    st.write(
        "Add subjects, topics, priorities, "
        "study durations, and deadlines."
    )


with step2:

    st.markdown("### 2️⃣ Study")

    st.write(
        "Start the timer and record your actual "
        "study sessions."
    )


with step3:

    st.markdown("### 3️⃣ Analyze")

    st.write(
        "Use charts and statistics to understand "
        "your productivity."
    )


with step4:

    st.markdown("### 4️⃣ Improve")

    st.write(
        "Use ML predictions and recommendations "
        "to improve your study routine."
    )


# --------------------------------
# Features
# --------------------------------

st.divider()

st.subheader("✨ Key Features")


feature_col1, feature_col2 = st.columns(2)


with feature_col1:

    st.markdown(
        """
        **📝 Smart Study Planner**

        • Create and manage study tasks  
        • Set priorities and deadlines  
        • Track completed and pending tasks  
        • Detect overdue tasks  
        """
    )

    st.markdown(
        """
        **⏱️ Focus Timer**

        • Custom study duration  
        • Pause and resume  
        • Record actual study time  
        • Save sessions automatically  
        """
    )


with feature_col2:

    st.markdown(
        """
        **📊 Productivity Analytics**

        • Study hours  
        • Subject-wise analysis  
        • Daily study trends  
        • Session history  
        """
    )

    st.markdown(
        """
        **🤖 Machine Learning**

        • Linear Regression model  
        • Performance prediction  
        • Study habit analysis  
        • Personalized recommendations  
        """
    )


# --------------------------------
# Technology Stack
# --------------------------------

st.divider()

st.subheader("🛠️ Built With")


tech1, tech2, tech3, tech4, tech5 = st.columns(5)


with tech1:

    st.markdown("### 🐍 Python")

    st.caption(
        "Core programming"
    )


with tech2:

    st.markdown("### 🎈 Streamlit")

    st.caption(
        "Web application"
    )


with tech3:

    st.markdown("### 🗄️ SQLite")

    st.caption(
        "Data storage"
    )


with tech4:

    st.markdown("### 📊 Pandas")

    st.caption(
        "Data analysis"
    )


with tech5:

    st.markdown("### 🤖 Scikit-learn")

    st.caption(
        "Machine learning"
    )


# --------------------------------
# Project Highlight
# --------------------------------

st.divider()

st.subheader("💡 Why StudyFlow?")


st.info(
    "StudyFlow combines software development, databases, "
    "data analysis, visualization, and machine learning "
    "into one practical student productivity application."
)


# --------------------------------
# Getting Started
# --------------------------------

st.divider()

st.subheader("🎯 Get Started")

st.write(
    "Use the sidebar to navigate through StudyFlow."
)

st.markdown(
    """
    **Recommended workflow:**

    📝 Add a task in **Planner**  
    ↓  
    ⏱️ Study using the **Timer**  
    ↓  
    📈 Check your **Analytics**  
    ↓  
    🤖 Get insights from **AI Prediction**
    """
)


# --------------------------------
# Footer
# --------------------------------

st.divider()

st.caption(
    "📚 StudyFlow  •  Plan • Study • Analyze • Improve"
)