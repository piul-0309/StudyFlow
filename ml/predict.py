import joblib
import pandas as pd


# Load trained model
model = joblib.load("ml/model.pkl")


def predict_performance(
    study_hours,
    tasks_completed,
    consistency,
    previous_performance
):
    """
    Predict performance score using the trained ML model.
    """

    input_data = pd.DataFrame({
        "study_hours": [study_hours],
        "tasks_completed": [tasks_completed],
        "consistency": [consistency],
        "previous_performance": [previous_performance]
    })

    prediction = model.predict(input_data)

    return prediction[0]