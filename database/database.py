import sqlite3


DATABASE_NAME = "studyflow.db"


def get_connection():
    """Create and return a connection to the database."""
    return sqlite3.connect(DATABASE_NAME)


def create_table():
    """Create the required database tables."""

    connection = get_connection()
    cursor = connection.cursor()

    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            priority TEXT NOT NULL,
            planned_date TEXT NOT NULL,
            planned_duration INTEGER NOT NULL,
            deadline TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    # Study sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def add_task(
    subject,
    topic,
    priority,
    planned_date,
    planned_duration,
    deadline
):
    """Add a new study task."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO tasks (
            subject,
            topic,
            priority,
            planned_date,
            planned_duration,
            deadline,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        subject,
        topic,
        priority,
        str(planned_date),
        planned_duration,
        str(deadline),
        "Pending"
    ))

    connection.commit()
    connection.close()


def get_tasks():
    """Return all study tasks."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            subject,
            topic,
            priority,
            planned_date,
            planned_duration,
            deadline,
            status
        FROM tasks
        ORDER BY planned_date
    """)

    tasks = cursor.fetchall()

    connection.close()

    return tasks


def update_task_status(task_id, status):
    """Update the status of a task."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = ?
        WHERE id = ?
    """, (status, task_id))

    connection.commit()
    connection.close()


def add_study_session(
    subject,
    topic,
    start_time,
    end_time,
    duration_minutes
):
    """Save a completed study session."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO study_sessions (
            subject,
            topic,
            start_time,
            end_time,
            duration_minutes
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        subject,
        topic,
        start_time,
        end_time,
        duration_minutes
    ))

    connection.commit()
    connection.close()


def get_study_sessions():
    """Return all recorded study sessions."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            subject,
            topic,
            start_time,
            end_time,
            duration_minutes
        FROM study_sessions
        ORDER BY start_time DESC
    """)

    sessions = cursor.fetchall()

    connection.close()

    return sessions