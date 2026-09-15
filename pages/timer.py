import streamlit as st
import time
from datetime import datetime

from database.database import (
    create_table,
    add_study_session
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="StudyFlow Focus Timer",
    page_icon="⏱️",
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
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* =====================================================
   HERO
   ===================================================== */

.timer-hero {
    text-align: center;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
}

.timer-title {
    font-size: 2rem;
    font-weight: 750;
}

.timer-subtitle {
    font-size: 0.9rem;
    opacity: 0.65;
    margin-top: 0.3rem;
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
   SETUP CARD
   ===================================================== */

.setup-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
}


/* =====================================================
   TIMER CARD
   ===================================================== */

.timer-card {
    background: linear-gradient(
        145deg,
        #F5F3FF,
        #FFFFFF
    );

    border: 1px solid #DDD6FE;

    border-radius: 28px;

    padding: 2.5rem;

    text-align: center;

    box-shadow:
        0 12px 30px rgba(108, 99, 255, 0.12);

    margin-top: 1rem;
}


.timer-status {
    color: #6C63FF;

    font-size: 0.8rem;

    font-weight: 750;

    letter-spacing: 0.08em;
}


.timer-display {
    color: #111827;

    font-size: 5rem;

    font-weight: 800;

    letter-spacing: 0.04em;

    margin: 0.8rem 0;
}


.timer-task {
    color: #6B7280;

    font-size: 0.9rem;
}


/* =====================================================
   INFO CARDS
   ===================================================== */

.info-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 18px;

    padding: 1.2rem;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.04);
}


.info-label {
    color: #6B7280;

    font-size: 0.75rem;

    font-weight: 700;
}


.info-value {
    color: #111827;

    font-size: 1.05rem;

    font-weight: 700;

    margin-top: 0.25rem;
}


/* =====================================================
   FOCUS TIPS
   ===================================================== */

.tip-card {
    background: #FFFFFF;

    border: 1px solid #E5E7EB;

    border-radius: 18px;

    padding: 1.25rem;

    min-height: 145px;

    box-shadow:
        0 5px 16px rgba(0, 0, 0, 0.04);
}


.tip-icon {
    font-size: 1.5rem;
}


.tip-title {
    color: #111827;

    font-weight: 700;

    margin-top: 0.4rem;
}


.tip-text {
    color: #6B7280;

    font-size: 0.8rem;

    line-height: 1.5;

    margin-top: 0.25rem;
}


/* =====================================================
   BUTTONS
   ===================================================== */

.stButton > button {
    border-radius: 12px;

    min-height: 44px;

    font-weight: 650;
}


/* =====================================================
   FOOTER
   ===================================================== */

.timer-footer {
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
# SESSION STATE
# =========================================================

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "timer_paused" not in st.session_state:
    st.session_state.timer_paused = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed_before_pause" not in st.session_state:
    st.session_state.elapsed_before_pause = 0

if "timer_subject" not in st.session_state:
    st.session_state.timer_subject = ""

if "timer_topic" not in st.session_state:
    st.session_state.timer_topic = ""

if "timer_duration" not in st.session_state:
    st.session_state.timer_duration = 25


# =========================================================
# HERO
# =========================================================

st.markdown(
    '<div class="timer-hero">'
    '<div class="timer-title">'
    '⏱️ Focus Timer'
    '</div>'
    '<div class="timer-subtitle">'
    'Block distractions, focus on one task, and make your study time count.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# STUDY SETUP
# =========================================================

if not st.session_state.timer_running:

    st.markdown(
        '<div class="section-title">'
        '📚 What are you studying?'
        '</div>'
        '<div class="section-subtitle">'
        'Choose what you want to focus on during this session.'
        '</div>',
        unsafe_allow_html=True
    )


    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            subject = st.text_input(
                "📚 Subject",
                placeholder="e.g. Data Structures"
            )

        with col2:

            topic = st.text_input(
                "📖 Topic",
                placeholder="e.g. Binary Search"
            )


    st.markdown(
        '<div class="section-title">'
        '⚙️ Session Settings'
        '</div>',
        unsafe_allow_html=True
    )


    duration_minutes = st.number_input(
        "Study Duration (minutes)",
        min_value=1,
        max_value=180,
        value=25,
        step=5,
        format="%d"
    )


else:

    subject = st.session_state.timer_subject

    topic = st.session_state.timer_topic

    duration_minutes = st.session_state.timer_duration


# =========================================================
# START SESSION
# =========================================================

if not st.session_state.timer_running:

    st.write("")

    if st.button(
        "▶️ Start Focus Session",
        use_container_width=True
    ):

        if not subject:

            st.error(
                "Please enter a subject."
            )

        elif not topic:

            st.error(
                "Please enter a topic."
            )

        else:

            st.session_state.timer_subject = subject

            st.session_state.timer_topic = topic

            st.session_state.timer_duration = duration_minutes

            st.session_state.timer_running = True

            st.session_state.timer_paused = False

            st.session_state.start_time = datetime.now()

            st.session_state.elapsed_before_pause = 0

            st.rerun()


# =========================================================
# RUNNING TIMER
# =========================================================

if st.session_state.timer_running:

    subject = st.session_state.timer_subject

    topic = st.session_state.timer_topic

    duration_minutes = st.session_state.timer_duration


    # =====================================================
    # CALCULATE ELAPSED TIME
    # =====================================================

    if st.session_state.timer_paused:

        elapsed_seconds = (
            st.session_state.elapsed_before_pause
        )

    else:

        current_time = datetime.now()

        elapsed_seconds = (
            st.session_state.elapsed_before_pause
            +
            int(
                (
                    current_time
                    -
                    st.session_state.start_time
                ).total_seconds()
            )
        )


    total_seconds = duration_minutes * 60

    remaining_seconds = max(
        total_seconds - elapsed_seconds,
        0
    )


    minutes = remaining_seconds // 60

    seconds = remaining_seconds % 60


    progress = min(
        elapsed_seconds / total_seconds,
        1.0
    )


    # =====================================================
    # STATUS
    # =====================================================

    if st.session_state.timer_paused:

        status = "SESSION PAUSED ⏸️"

    else:

        status = "FOCUS SESSION 🔥"


    # =====================================================
    # TIMER DISPLAY
    # =====================================================

    st.markdown(
        '<div class="timer-card">'
        f'<div class="timer-status">{status}</div>'
        f'<div class="timer-display">'
        f'{minutes:02d}:{seconds:02d}'
        f'</div>'
        f'<div class="timer-task">'
        f'📚 {subject} &nbsp;•&nbsp; 📖 {topic}'
        f'</div>'
        '</div>',
        unsafe_allow_html=True
    )


    st.progress(progress)


    st.caption(
        f"{elapsed_seconds // 60} minute(s) completed "
        f"of {duration_minutes} minute(s)"
    )


    # =====================================================
    # SESSION INFORMATION
    # =====================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            '<div class="info-card">'
            '<div class="info-label">'
            'SUBJECT'
            '</div>'
            '<div class="info-value">'
            f'📚 {subject}'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            '<div class="info-card">'
            '<div class="info-label">'
            'TOPIC'
            '</div>'
            '<div class="info-value">'
            f'📖 {topic}'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            '<div class="info-card">'
            '<div class="info-label">'
            'PLANNED DURATION'
            '</div>'
            '<div class="info-value">'
            f'⏱️ {duration_minutes} min'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # SESSION COMPLETED
    # =====================================================

    if remaining_seconds == 0:

        end_time = datetime.now()


        if st.session_state.timer_paused:

            actual_seconds = (
                st.session_state.elapsed_before_pause
            )

        else:

            actual_seconds = (
                st.session_state.elapsed_before_pause
                +
                int(
                    (
                        end_time
                        -
                        st.session_state.start_time
                    ).total_seconds()
                )
            )


        actual_duration = max(
            int(actual_seconds / 60),
            1
        )


        add_study_session(
            subject,
            topic,
            st.session_state.start_time.isoformat(),
            end_time.isoformat(),
            actual_duration
        )


        st.balloons()


        st.success(
            f"🎉 Session completed! "
            f"{actual_duration} minute(s) recorded."
        )


        st.session_state.timer_running = False

        st.session_state.timer_paused = False

        st.session_state.start_time = None

        st.session_state.elapsed_before_pause = 0

        st.rerun()


    # =====================================================
    # TIMER CONTROLS
    # =====================================================

    st.write("")


    control1, control2, control3 = st.columns(3)


    # =====================================================
    # PAUSE / RESUME
    # =====================================================

    with control1:

        if not st.session_state.timer_paused:

            if st.button(
                "⏸️ Pause",
                use_container_width=True
            ):

                current_time = datetime.now()

                st.session_state.elapsed_before_pause += int(
                    (
                        current_time
                        -
                        st.session_state.start_time
                    ).total_seconds()
                )

                st.session_state.timer_paused = True

                st.rerun()

        else:

            if st.button(
                "▶️ Resume",
                use_container_width=True
            ):

                st.session_state.timer_paused = False

                st.session_state.start_time = datetime.now()

                st.rerun()


    # =====================================================
    # STOP & SAVE
    # =====================================================

    with control2:

        if st.button(
            "⏹️ Stop & Save",
            use_container_width=True
        ):

            end_time = datetime.now()


            if st.session_state.timer_paused:

                actual_seconds = (
                    st.session_state.elapsed_before_pause
                )

            else:

                current_elapsed = int(
                    (
                        end_time
                        -
                        st.session_state.start_time
                    ).total_seconds()
                )

                actual_seconds = (
                    st.session_state.elapsed_before_pause
                    +
                    current_elapsed
                )


            actual_duration = max(
                int(actual_seconds / 60),
                1
            )


            add_study_session(
                subject,
                topic,
                st.session_state.start_time.isoformat(),
                end_time.isoformat(),
                actual_duration
            )


            st.session_state.timer_running = False

            st.session_state.timer_paused = False

            st.session_state.start_time = None

            st.session_state.elapsed_before_pause = 0


            st.success(
                f"🎉 Session saved — "
                f"{actual_duration} minute(s)"
            )

            st.rerun()


    # =====================================================
    # RESET
    # =====================================================

    with control3:

        if st.button(
            "🔄 Reset",
            use_container_width=True
        ):

            st.session_state.timer_running = False

            st.session_state.timer_paused = False

            st.session_state.start_time = None

            st.session_state.elapsed_before_pause = 0

            st.rerun()


    # =====================================================
    # TIMER LOOP
    # =====================================================

    if not st.session_state.timer_paused:

        time.sleep(1)

        st.rerun()


# =========================================================
# FOCUS TIPS
# =========================================================

if not st.session_state.timer_running:

    st.markdown(
        '<div class="section-title">'
        '💡 Focus Tips'
        '</div>'
        '<div class="section-subtitle">'
        'A few simple habits to make your study sessions better.'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            '<div class="tip-card">'
            '<div class="tip-icon">🎯</div>'
            '<div class="tip-title">One Task</div>'
            '<div class="tip-text">'
            'Choose one topic and focus only on that task '
            'during your session.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            '<div class="tip-card">'
            '<div class="tip-icon">📵</div>'
            '<div class="tip-title">Remove Distractions</div>'
            '<div class="tip-text">'
            'Keep unnecessary notifications, social media, '
            'and distractions away while studying.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            '<div class="tip-card">'
            '<div class="tip-icon">☕</div>'
            '<div class="tip-title">Take Breaks</div>'
            '<div class="tip-text">'
            'Take short breaks between focused sessions '
            'to maintain concentration.'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="timer-footer">'
    '⏱️ StudyFlow Focus Timer &nbsp;•&nbsp; '
    'Focus &nbsp;•&nbsp; Study &nbsp;•&nbsp; Improve'
    '</div>',
    unsafe_allow_html=True
)