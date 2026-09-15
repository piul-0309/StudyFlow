import streamlit as st

from ml.predict import predict_performance
from utils.helpers import generate_recommendations


# --------------------------------
# Page Title
# --------------------------------

st.title("🤖 AI Performance Prediction")

st.write(
    "Use your study habits to predict your academic "
    "performance and receive personalized recommendations."
)


# --------------------------------
# Input Section
# --------------------------------

st.subheader("📊 Your Study Information")

col1, col2 = st.columns(2)


with col1:

    study_hours = st.number_input(
        "⏱️ Daily Study Hours",
        min_value=0.0,
        max_value=24.0,
        value=2.0,
        step=0.5
    )

    tasks_completed = st.number_input(
        "📝 Tasks Completed",
        min_value=0,
        max_value=50,
        value=5,
        step=1
    )


with col2:

    consistency = st.slider(
        "📅 Study Consistency (%)",
        min_value=0,
        max_value=100,
        value=70
    )

    previous_performance = st.slider(
        "📈 Previous Performance Score",
        min_value=0,
        max_value=100,
        value=65
    )


# --------------------------------
# Study Information Summary
# --------------------------------

st.divider()

st.subheader("📋 Your Current Study Pattern")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Study Hours",
        f"{study_hours:.1f} h"
    )

with col2:
    st.metric(
        "Tasks",
        tasks_completed
    )

with col3:
    st.metric(
        "Consistency",
        f"{consistency}%"
    )

with col4:
    st.metric(
        "Previous Score",
        f"{previous_performance}/100"
    )


# --------------------------------
# Prediction Button
# --------------------------------

st.divider()

if st.button(
    "🔮 Predict My Performance",
    use_container_width=True
):

    # --------------------------------
    # ML Prediction
    # --------------------------------

    prediction = predict_performance(
        study_hours,
        tasks_completed,
        consistency,
        previous_performance
    )


    # Keep prediction between 0 and 100

    prediction = max(
        0,
        min(100, prediction)
    )


    # --------------------------------
    # Prediction Result
    # --------------------------------

    st.subheader("🎯 Prediction Result")

    st.metric(
        "Predicted Performance Score",
        f"{prediction:.1f}/100"
    )


    # --------------------------------
    # Prediction Progress
    # --------------------------------

    st.progress(
        prediction / 100
    )


    # --------------------------------
    # Performance Category
    # --------------------------------

    if prediction >= 80:

        st.success(
            "🏆 Excellent! Your current study pattern "
            "is associated with strong performance."
        )

        performance_level = "Excellent"

    elif prediction >= 60:

        st.warning(
            "👍 Good progress! There is still room "
            "to improve your study pattern."
        )

        performance_level = "Good"

    else:

        st.error(
            "💪 Your predicted score is currently low. "
            "Improving your study habits can help."
        )

        performance_level = "Needs Improvement"


    st.write(
        f"**Performance Level:** {performance_level}"
    )


    # --------------------------------
    # Recommendations
    # --------------------------------

    st.divider()

    st.subheader("💡 Smart Recommendations")

    recommendations = generate_recommendations(
        study_hours,
        tasks_completed,
        consistency,
        prediction
    )


    for recommendation in recommendations:

        st.write(
            f"• {recommendation}"
        )


    # --------------------------------
    # Improvement Tips
    # --------------------------------

    st.divider()

    st.subheader("🚀 Focus Areas")

    if study_hours < 2:

        st.info(
            "⏱️ **Study Time:** "
            "Try gradually increasing your daily study time."
        )

    else:

        st.success(
            "⏱️ **Study Time:** "
            "Your study duration is on a good track."
        )


    if tasks_completed < 3:

        st.info(
            "📝 **Task Completion:** "
            "Try completing at least 3 planned tasks regularly."
        )

    else:

        st.success(
            "📝 **Task Completion:** "
            "Good job completing your planned tasks!"
        )


    if consistency < 60:

        st.info(
            "📅 **Consistency:** "
            "Create a fixed study routine and follow it daily."
        )

    elif consistency < 80:

        st.warning(
            "📅 **Consistency:** "
            "You're improving. Try reaching 80%+ consistency."
        )

    else:

        st.success(
            "📅 **Consistency:** "
            "Excellent! You're maintaining a strong routine."
        )


    # --------------------------------
    # ML Explanation
    # --------------------------------

    st.divider()

    with st.expander("🧠 How does this prediction work?"):

        st.write(
            "StudyFlow uses a **Linear Regression** machine "
            "learning model to estimate your performance score."
        )

        st.write(
            "The model considers four inputs:"
        )

        st.write(
            "1. ⏱️ Study Hours"
        )

        st.write(
            "2. 📝 Tasks Completed"
        )

        st.write(
            "3. 📅 Study Consistency"
        )

        st.write(
            "4. 📈 Previous Performance"
        )

        st.write(
            "The model learns the relationship between these "
            "study habits and the performance scores in the "
            "training dataset."
        )

        st.write(
            "After training, the model can use new study "
            "information to predict a performance score."
        )