import streamlit as st

from ml.predict import predict_performance
from utils.helpers import generate_recommendations


# --------------------------------
# Page Header
# --------------------------------

st.title("🤖 AI Performance Prediction")

st.caption(
    "Use your study habits to estimate performance "
    "and get personalized study recommendations."
)


# --------------------------------
# Input Section
# --------------------------------

st.subheader("📊 Your Study Pattern")

with st.container(border=True):

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
            "📅 Study Consistency",
            min_value=0,
            max_value=100,
            value=70,
            help="How consistently you follow your study routine."
        )

        previous_performance = st.slider(
            "📈 Previous Performance",
            min_value=0,
            max_value=100,
            value=65,
            help="Your previous academic performance score."
        )


# --------------------------------
# Input Summary
# --------------------------------

st.divider()

st.subheader("📋 Study Pattern Summary")

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
# Prediction
# --------------------------------

st.divider()

if st.button(
    "🔮 Predict My Performance",
    use_container_width=True
):

    # --------------------------------
    # Run ML Model
    # --------------------------------

    prediction = predict_performance(
        study_hours,
        tasks_completed,
        consistency,
        previous_performance
    )


    # Keep prediction within 0-100

    prediction = max(
        0,
        min(100, prediction)
    )


    # --------------------------------
    # Prediction Result
    # --------------------------------

    st.subheader("🎯 Your Prediction")


    result_col1, result_col2 = st.columns(
        [1, 2]
    )


    with result_col1:

        st.metric(
            "Predicted Performance",
            f"{prediction:.1f}/100"
        )


    with result_col2:

        st.progress(
            prediction / 100
        )

        st.caption(
            f"{prediction:.1f}% predicted performance"
        )


    # --------------------------------
    # Performance Category
    # --------------------------------

    if prediction >= 80:

        performance_level = "Excellent 🏆"

        st.success(
            "🌟 Excellent! Your current study pattern "
            "looks strong."
        )

    elif prediction >= 60:

        performance_level = "Good 👍"

        st.warning(
            "👍 Good progress! You can still improve "
            "your study habits."
        )

    else:

        performance_level = "Needs Improvement 💪"

        st.error(
            "💪 Your predicted score is currently low. "
            "Focus on improving your study routine."
        )


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

        with st.container(border=True):

            st.write(
                recommendation
            )


    # --------------------------------
    # Focus Areas
    # --------------------------------

    st.divider()

    st.subheader("🚀 Focus Areas")


    focus_col1, focus_col2, focus_col3 = st.columns(3)


    with focus_col1:

        st.markdown("### ⏱️ Study Time")

        if study_hours < 2:

            st.warning(
                "Try gradually increasing your daily study time."
            )

        else:

            st.success(
                "Your study duration is on a good track."
            )


    with focus_col2:

        st.markdown("### 📝 Tasks")

        if tasks_completed < 3:

            st.warning(
                "Try completing at least 3 tasks regularly."
            )

        else:

            st.success(
                "Good task completion!"
            )


    with focus_col3:

        st.markdown("### 📅 Consistency")

        if consistency < 60:

            st.warning(
                "Try following a fixed study routine."
            )

        elif consistency < 80:

            st.info(
                "You're improving. Aim for 80%+."
            )

        else:

            st.success(
                "Excellent consistency!"
            )


    # --------------------------------
    # ML Explanation
    # --------------------------------

    st.divider()

    with st.expander("🧠 How does StudyFlow predict performance?"):

        st.write(
            "StudyFlow uses a **Linear Regression** "
            "machine learning model."
        )

        st.write(
            "The model was trained using four features:"
        )

        st.write(
            "• ⏱️ Study Hours"
        )

        st.write(
            "• 📝 Tasks Completed"
        )

        st.write(
            "• 📅 Study Consistency"
        )

        st.write(
            "• 📈 Previous Performance"
        )

        st.write(
            "The model learns the relationship between "
            "these study habits and performance scores."
        )

        st.write(
            "When you enter new values, the trained model "
            "uses those values to estimate your performance."
        )