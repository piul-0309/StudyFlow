import streamlit as st
import time
from datetime import datetime

from database.database import (
    create_table,
    add_study_session
)


# --------------------------------
# Create Database Tables
# --------------------------------

create_table()


# --------------------------------
# Page Title
# --------------------------------

st.title("⏱️ Study Timer")

st.write(
    "Focus on your study session and track your actual study time."
)


# --------------------------------
# Session Details
# --------------------------------

st.subheader("📚 Session Details")

subject = st.text_input(
    "Subject",
    placeholder="e.g. Data Structures"
)

topic = st.text_input(
    "Topic",
    placeholder="e.g. Binary Search"
)


# --------------------------------
# Timer Settings
# --------------------------------

st.subheader("⚙️ Timer Settings")

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

if "pause_time" not in st.session_state:
    st.session_state.pause_time = None


# --------------------------------
# Start Timer
# --------------------------------

if not st.session_state.timer_running:

    if st.button(
        "▶️ Start Study Session",
        use_container_width=True
    ):

        if subject and topic:

            st.session_state.timer_running = True
            st.session_state.timer_paused = False

            st.session_state.start_time = datetime.now()

            st.session_state.elapsed_before_pause = 0

            st.session_state.pause_time = None

            st.rerun()

        else:

            st.error(
                "Please enter both Subject and Topic."
            )


# --------------------------------
# Running Timer
# --------------------------------

if st.session_state.timer_running:

    st.success(
        "🔥 Study session is running!"
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
    # Total Timer Duration
    # --------------------------------

    total_seconds = duration_minutes * 60


    remaining_seconds = max(
        total_seconds - elapsed_seconds,
        0
    )


    # --------------------------------
    # Convert Time
    # --------------------------------

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60


    # --------------------------------
    # Display Timer
    # --------------------------------

    st.metric(
        "⏳ Time Remaining",
        f"{minutes:02d}:{seconds:02d}"
    )


    # --------------------------------
    # Progress Bar
    # --------------------------------

    progress = min(
        elapsed_seconds / total_seconds,
        1.0
    )

    st.progress(progress)


    # --------------------------------
    # Timer Completed
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


        st.session_state.timer_running = False

        st.session_state.timer_paused = False

        st.session_state.start_time = None

        st.session_state.elapsed_before_pause = 0

        st.session_state.pause_time = None


    # --------------------------------
    # Timer Controls
    # --------------------------------

    else:

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

                    st.session_state.pause_time = current_time

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
        # Stop Session
        # --------------------------------

        with col2:

            if st.button(
                "⏹️ Stop",
                use_container_width=True
            ):

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


                st.session_state.timer_running = False

                st.session_state.timer_paused = False

                st.session_state.start_time = None

                st.session_state.elapsed_before_pause = 0

                st.session_state.pause_time = None


                st.success(
                    f"Study session saved! ⏱️ "
                    f"{actual_duration} minute(s)"
                )

                st.rerun()


        # --------------------------------
        # Reset Timer
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

                st.session_state.pause_time = None

                st.rerun()


        # --------------------------------
        # Paused Message
        # --------------------------------

        if st.session_state.timer_paused:

            st.warning(
                "⏸️ Timer is paused. Click Resume to continue."
            )

        else:

            time.sleep(1)

            st.rerun()