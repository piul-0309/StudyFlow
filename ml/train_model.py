import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import joblib


# --------------------------------
# 1. Create Sample Study Dataset
# --------------------------------

data = {
    "study_hours": [
        1.0, 1.5, 2.0, 2.5, 3.0,
        3.5, 4.0, 4.5, 5.0, 5.5,
        2.0, 3.0, 4.0, 1.5, 5.0,
        2.5, 3.5, 4.5, 6.0, 6.5
    ],

    "tasks_completed": [
        2, 3, 4, 5, 6,
        7, 8, 9, 10, 11,
        3, 6, 8, 2, 10,
        5, 7, 9, 12, 13
    ],

    "consistency": [
        50, 55, 60, 65, 70,
        75, 80, 85, 90, 95,
        60, 70, 80, 55, 90,
        65, 75, 85, 95, 98
    ],

    "previous_performance": [
        50, 52, 55, 58, 60,
        65, 68, 70, 75, 78,
        54, 62, 70, 51, 74,
        59, 66, 72, 80, 85
    ],

    "performance_score": [
        52, 55, 59, 63, 67,
        72, 76, 80, 85, 88,
        58, 68, 77, 54, 84,
        64, 71, 79, 90, 94
    ]
}


df = pd.DataFrame(data)


# --------------------------------
# 2. Save Dataset
# --------------------------------

df.to_csv(
    "data/study_data.csv",
    index=False
)

print("Dataset created successfully!")
print(df.head())


# --------------------------------
# 3. Select Features and Target
# --------------------------------

X = df[
    [
        "study_hours",
        "tasks_completed",
        "consistency",
        "previous_performance"
    ]
]

y = df["performance_score"]


# --------------------------------
# 4. Split Dataset
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# --------------------------------
# 5. Train Model
# --------------------------------

model = LinearRegression()

model.fit(
    X_train,
    y_train
)


# --------------------------------
# 6. Test Model
# --------------------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(
    y_test,
    predictions
)

print(f"Mean Absolute Error: {mae:.2f}")


# --------------------------------
# 7. Save Model
# --------------------------------

joblib.dump(
    model,
    "ml/model.pkl"
)

print("Model saved successfully!")