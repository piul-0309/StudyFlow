import streamlit as st
import time
from datetime import datetime

from database.database import (
    create_table,
    add_study_session
)


# --------------------------------
# Database
# --------------------------------

create_table()


# --------------------------------
# Page Header
# --------------------------------

st.title("⏱️ Study Timer")

st.caption(
    "Focus on one task at a time and track your actual study time."
)


# --------------------------------
# Session Details
# --------------------------------

st.subheader("📚 What are you studying?")

col1, col2 = st.columns(2)

with col1:

    subject = st.text_input(
        "Subject",
        placeholder="e.g. Data Structures"
    )

with col2:

    topic = st.text_input(
        "Topic",
        placeholder="e.g. Binary Search"
    )


# --------------------------------
# Timer Settings
# --------------------------------

st.subheader("⚙️ Session Settings")

duration_minutes = st.number_input(
    "Study Duration (minutes)",
    min_value=1,
    max_value=180,
    value=25,
    step=5
)


# --------------------------------
# Session State
# --------------------------------

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

if "timer_paused" not in st.session_state:
    st.session_state.timer_paused = False

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if "elapsed_before_pause" not in st.session_state:
    st.session_state.elapsed_before_pause = 0


# --------------------------------
# Start Session
# --------------------------------

if not st.session_state.timer_running:

    st.divider()

    if st.button(
        "▶️ Start Study Session",
        use_container_width=True
    ):

        if not subject or not topic:

            st.error(
                "Please enter both Subject and Topic."
            )

        else:

            st.session_state.timer_running = True
            st.session_state.timer_paused = False
            st.session_state.start_time = datetime.now()
            st.session_state.elapsed_before_pause = 0

            st.rerun()


# --------------------------------
# Active Timer
# --------------------------------

if st.session_state.timer_running:

    st.divider()

    if st.session_state.timer_paused:

        st.warning(
            "⏸️ Study session paused"
        )

    else:

        st.success(
            "🔥 Study session in progress"
        )


    # --------------------------------
    # Calculate Elapsed Time
    # --------------------------------

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


    # --------------------------------
    # Timer Calculation
    # --------------------------------

    total_seconds = duration_minutes * 60

    remaining_seconds = max(
        total_seconds - elapsed_seconds,
        0
    )


    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60


    # --------------------------------
    # Timer Display
    # --------------------------------

    st.subheader(
        f"⏳ {minutes:02d}:{seconds:02d}"
    )


    progress = min(
        elapsed_seconds / total_seconds,
        1.0
    )

    st.progress(progress)


    st.caption(
        f"{elapsed_seconds // 60} minute(s) completed "
        f"of {duration_minutes} minute(s)"
    )


    # --------------------------------
    # Session Completed
    # --------------------------------

    if remaining_seconds == 0:

        end_time = datetime.now()

        actual_duration = int(
            (
                end_time
                -
                st.session_state.start_time
            ).total_seconds() / 60
        )

        actual_duration += int(
            st.session_state.elapsed_before_pause / 60
        )

        actual_duration = max(
            actual_duration,
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
            "🎉 Study session completed and saved!"
        )


        st.metric(
            "⏱️ Session Duration",
            f"{actual_duration} minute(s)"
        )


        st.session_state.timer_running = False
        st.session_state.timer_paused = False
        st.session_state.start_time = None
        st.session_state.elapsed_before_pause = 0


    # --------------------------------
    # Timer Controls
    # --------------------------------

    else:

        st.divider()

        col1, col2, col3 = st.columns(3)


        # --------------------------------
        # Pause / Resume
        # --------------------------------

        with col1:

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


        # --------------------------------
        # Stop
        # --------------------------------

        with col2:

            if st.button(
                "⏹️ Stop",
                use_container_width=True
            ):

                end_time = datetime.now()

                if st.session_state.timer_paused:

                    actual_duration = int(
                        st.session_state.elapsed_before_pause
                        / 60
                    )

                else:

                    current_elapsed = int(
                        (
                            end_time
                            -
                            st.session_state.start_time
                        ).total_seconds()
                    )

                    actual_duration = int(
                        (
                            st.session_state.elapsed_before_pause
                            +
                            current_elapsed
                        ) / 60
                    )


                actual_duration = max(
                    actual_duration,
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


        # --------------------------------
        # Reset
        # --------------------------------

        with col3:

            if st.button(
                "🔄 Reset",
                use_container_width=True
            ):

                st.session_state.timer_running = False
                st.session_state.timer_paused = False
                st.session_state.start_time = None
                st.session_state.elapsed_before_pause = 0

                st.rerun()


        # --------------------------------
        # Automatic Refresh
        # --------------------------------

        if not st.session_state.timer_paused:

            time.sleep(1)

            st.rerun()


# --------------------------------
# Study Tips
# --------------------------------

if not st.session_state.timer_running:

    st.divider()

    st.subheader("💡 Focus Tips")

    tip1, tip2, tip3 = st.columns(3)

    with tip1:

        st.markdown("### 🎯 One Task")

        st.caption(
            "Focus on one topic during each session."
        )

    with tip2:

        st.markdown("### 📵 Remove Distractions")

        st.caption(
            "Keep unnecessary notifications and distractions away."
        )

    with tip3:

        st.markdown("### ☕ Take Breaks")

        st.caption(
            "Take short breaks between longer study sessions."
        )