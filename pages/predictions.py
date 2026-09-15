import streamlit as st

from ml.predict import predict_performance
from utils.helpers import generate_recommendations


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StudyFlow AI Prediction",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =====================================================
   HERO
   ===================================================== */

.ai-hero {
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


.ai-title {
    font-size: 2rem;
    font-weight: 750;
}


.ai-subtitle {
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
   INPUT CARD
   ===================================================== */

.input-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 20px;

    padding: 1.4rem;

    box-shadow:
        0 6px 20px rgba(0, 0, 0, 0.05);
}


/* =====================================================
   SUMMARY CARDS
   ===================================================== */

.summary-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 17px;

    padding: 1.1rem;

    min-height: 110px;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.04);
}


.summary-icon {
    font-size: 1.25rem;
}


.summary-label {
    color: #6B7280;

    font-size: 0.73rem;

    font-weight: 700;

    margin-top: 0.3rem;
}


.summary-value {
    color: #111827;

    font-size: 1.45rem;

    font-weight: 750;

    margin-top: 0.15rem;
}


/* =====================================================
   RESULT CARD
   ===================================================== */

.result-card {
    background: linear-gradient(
        145deg,
        #F5F3FF,
        #FFFFFF
    );

    border: 1px solid #DDD6FE;

    border-radius: 24px;

    padding: 1.8rem;

    box-shadow:
        0 10px 25px rgba(108, 99, 255, 0.10);

    text-align: center;
}


.result-label {
    color: #6C63FF;

    font-size: 0.78rem;

    font-weight: 750;

    letter-spacing: 0.06em;
}


.result-score {
    color: #111827;

    font-size: 3.5rem;

    font-weight: 800;

    margin-top: 0.3rem;
}


/* =====================================================
   RECOMMENDATION
   ===================================================== */

.recommendation-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 15px;

    padding: 1rem;

    margin-bottom: 0.7rem;

    box-shadow:
        0 4px 12px rgba(0, 0, 0, 0.035);
}


/* =====================================================
   FOCUS CARD
   ===================================================== */

.focus-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 18px;

    padding: 1.2rem;

    min-height: 140px;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.04);
}


.focus-icon {
    font-size: 1.4rem;
}


.focus-title {
    font-weight: 700;

    margin-top: 0.35rem;
}


.focus-text {
    color: #6B7280;

    font-size: 0.8rem;

    margin-top: 0.35rem;
}


/* =====================================================
   FOOTER
   ===================================================== */

.ai-footer {
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
    '<div class="ai-hero">'
    '<div class="ai-title">'
    '🤖 AI Performance Prediction'
    '</div>'
    '<div class="ai-subtitle">'
    'Use your study habits to estimate your performance '
    'and receive personalized recommendations.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# STUDY PATTERN INPUT
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📊 Your Study Pattern'
    '</div>'
    '<div class="section-subtitle">'
    'Enter your current study habits to generate a prediction.'
    '</div>',
    unsafe_allow_html=True
)


with st.container(border=True):

    col1, col2 = st.columns(2)


    # -----------------------------------------------------
    # LEFT COLUMN
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # RIGHT COLUMN
    # -----------------------------------------------------

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


# =========================================================
# STUDY SUMMARY
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📋 Study Pattern Summary'
    '</div>',
    unsafe_allow_html=True
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        '<div class="summary-card">'
        '<div class="summary-icon">⏱️</div>'
        '<div class="summary-label">STUDY HOURS</div>'
        f'<div class="summary-value">'
        f'{study_hours:.1f} h'
        f'</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        '<div class="summary-card">'
        '<div class="summary-icon">📝</div>'
        '<div class="summary-label">TASKS</div>'
        f'<div class="summary-value">'
        f'{tasks_completed}'
        f'</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        '<div class="summary-card">'
        '<div class="summary-icon">📅</div>'
        '<div class="summary-label">CONSISTENCY</div>'
        f'<div class="summary-value">'
        f'{consistency}%'
        f'</div>'
        '</div>',
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        '<div class="summary-card">'
        '<div class="summary-icon">📈</div>'
        '<div class="summary-label">PREVIOUS SCORE</div>'
        f'<div class="summary-value">'
        f'{previous_performance}'
        f'</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# PREDICT BUTTON
# =========================================================

st.write("")

if st.button(
    "🔮 Predict My Performance",
    use_container_width=True
):

    # -----------------------------------------------------
    # MODEL PREDICTION
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # PERFORMANCE LEVEL
    # -----------------------------------------------------

    if prediction >= 80:

        performance_level = "Excellent 🏆"

        message = (
            "Your current study pattern looks strong. "
            "Keep maintaining these habits."
        )

    elif prediction >= 60:

        performance_level = "Good 👍"

        message = (
            "You are on a good track. "
            "A little more consistency can help you improve."
        )

    else:

        performance_level = "Needs Improvement 💪"

        message = (
            "Your predicted performance is currently low. "
            "Focus on study time, consistency, and task completion."
        )


    # =====================================================
    # RESULT
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🎯 Prediction Result'
        '</div>',
        unsafe_allow_html=True
    )


    result_col1, result_col2 = st.columns(
        [1, 2]
    )


    with result_col1:

        st.markdown(
            '<div class="result-card">'
            '<div class="result-label">'
            'PREDICTED PERFORMANCE'
            '</div>'
            f'<div class="result-score">'
            f'{prediction:.1f}'
            '</div>'
            '<div>'
            'out of 100'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with result_col2:

        st.subheader(
            performance_level
        )

        st.write(message)

        st.progress(
            prediction / 100
        )

        st.caption(
            f"Predicted performance: "
            f"{prediction:.1f}%"
        )


    # =====================================================
    # RECOMMENDATIONS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '💡 Smart Recommendations'
        '</div>'
        '<div class="section-subtitle">'
        'Suggestions based on your current study pattern.'
        '</div>',
        unsafe_allow_html=True
    )


    recommendations = generate_recommendations(
        study_hours,
        tasks_completed,
        consistency,
        prediction
    )


    for recommendation in recommendations:

        st.markdown(
            '<div class="recommendation-card">'
            f'{recommendation}'
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # FOCUS AREAS
    # =====================================================

    st.markdown(
        '<div class="section-title">'
        '🚀 Focus Areas'
        '</div>',
        unsafe_allow_html=True
    )


    focus_col1, focus_col2, focus_col3 = st.columns(3)


    # -----------------------------------------------------
    # STUDY TIME
    # -----------------------------------------------------

    with focus_col1:

        if study_hours < 2:

            focus_message = (
                "Try gradually increasing your daily "
                "study time."
            )

        else:

            focus_message = (
                "Your study duration is on a good track."
            )


        st.markdown(
            '<div class="focus-card">'
            '<div class="focus-icon">⏱️</div>'
            '<div class="focus-title">'
            'Study Time'
            '</div>'
            f'<div class="focus-text">'
            f'{focus_message}'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # TASKS
    # -----------------------------------------------------

    with focus_col2:

        if tasks_completed < 3:

            focus_message = (
                "Try completing at least 3 planned "
                "tasks regularly."
            )

        else:

            focus_message = (
                "Good task completion. "
                "Keep setting achievable goals."
            )


        st.markdown(
            '<div class="focus-card">'
            '<div class="focus-icon">📝</div>'
            '<div class="focus-title">'
            'Task Completion'
            '</div>'
            f'<div class="focus-text">'
            f'{focus_message}'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # CONSISTENCY
    # -----------------------------------------------------

    with focus_col3:

        if consistency < 60:

            focus_message = (
                "Try following a fixed study routine."
            )

        elif consistency < 80:

            focus_message = (
                "You're improving. Aim for 80%+ consistency."
            )

        else:

            focus_message = (
                "Excellent consistency. "
                "Keep following your routine."
            )


        st.markdown(
            '<div class="focus-card">'
            '<div class="focus-icon">📅</div>'
            '<div class="focus-title">'
            'Consistency'
            '</div>'
            f'<div class="focus-text">'
            f'{focus_message}'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # HOW THE MODEL WORKS
    # =====================================================

    st.write("")

    with st.expander(
        "🧠 How does StudyFlow predict performance?"
    ):

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


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="ai-footer">'
    '🤖 StudyFlow AI &nbsp;•&nbsp; '
    'Predict &nbsp;•&nbsp; Recommend &nbsp;•&nbsp; Improve'
    '</div>',
    unsafe_allow_html=True
)