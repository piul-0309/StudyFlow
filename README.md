# 📚 StudyFlow

### Your Smart Study Planner & Productivity Assistant

StudyFlow is a Python-based study productivity application that helps students plan their studies, track study sessions, analyze their productivity, and receive machine-learning-based performance predictions.

---

## 🚀 Features

### 📝 Study Planner

- Add study tasks
- Add subjects and topics
- Set task priority
- Set planned study date
- Set planned study duration
- Set deadlines
- Mark tasks as completed
- Search and filter tasks
- Detect overdue tasks

### ⏱️ Study Timer

- Start focused study sessions
- Set custom study duration
- Pause and resume sessions
- Stop sessions manually
- Automatically save completed sessions
- Track actual study time

### 📈 Analytics

StudyFlow analyzes your study activity and displays:

- Total study hours
- Number of study sessions
- Completed tasks
- Pending tasks
- Subject-wise study time
- Daily study trends
- Study session history

### 🎯 Daily Study Goals

Users can set a daily study target and track their progress toward that goal.

### 🔥 Study Streak

StudyFlow calculates consecutive study days to help users maintain consistency.

### 🤖 ML Performance Prediction

StudyFlow uses **Linear Regression** to predict a student's performance score.

The model uses:

- Study hours
- Tasks completed
- Study consistency
- Previous performance

The predicted score is displayed on a scale of **0–100**.

### 💡 Smart Recommendations

Based on the user's study habits and predicted performance, StudyFlow provides personalized recommendations to improve:

- Study duration
- Task completion
- Consistency
- Overall performance

---

## 🧠 Machine Learning

The project uses a **Linear Regression** model from Scikit-learn.

### Input Features

```text
study_hours
tasks_completed
consistency
previous_performance