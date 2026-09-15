import pandas as pd


def sessions_to_dataframe(sessions):
    """Convert study sessions into a Pandas DataFrame."""

    columns = [
        "id",
        "subject",
        "topic",
        "start_time",
        "end_time",
        "duration_minutes"
    ]

    df = pd.DataFrame(sessions, columns=columns)

    if not df.empty:
        df["start_time"] = pd.to_datetime(df["start_time"])
        df["end_time"] = pd.to_datetime(df["end_time"])

        df["date"] = df["start_time"].dt.date

    return df


def get_total_study_minutes(df):
    """Calculate total study time."""

    if df.empty:
        return 0

    return df["duration_minutes"].sum()


def get_subject_summary(df):
    """Calculate study time for each subject."""

    if df.empty:
        return pd.DataFrame()

    summary = (
        df.groupby("subject")["duration_minutes"]
        .sum()
        .reset_index()
    )

    summary = summary.sort_values(
        "duration_minutes",
        ascending=False
    )

    return summary


def get_daily_summary(df):
    """Calculate study time for each day."""

    if df.empty:
        return pd.DataFrame()

    summary = (
        df.groupby("date")["duration_minutes"]
        .sum()
        .reset_index()
    )

    return summary