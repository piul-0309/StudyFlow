def generate_recommendations(
    study_hours,
    tasks_completed,
    consistency,
    predicted_score
):
    """
    Generate personalized study recommendations
    based on the student's study behavior.
    """

    recommendations = []

    # Study time recommendation
    if study_hours < 2:
        recommendations.append(
            "⏱️ Try increasing your daily study time to at least 2 hours."
        )

    elif study_hours >= 4:
        recommendations.append(
            "🌟 Great study duration! Make sure you take regular breaks."
        )

    else:
        recommendations.append(
            "👍 Your study duration is reasonable. Try to maintain it consistently."
        )


    # Task completion recommendation
    if tasks_completed < 3:
        recommendations.append(
            "📝 Try completing at least 3 planned tasks each study day."
        )

    else:
        recommendations.append(
            "✅ Good task completion! Keep setting achievable daily goals."
        )


    # Consistency recommendation
    if consistency < 60:
        recommendations.append(
            "📅 Your consistency is low. Try following a fixed study schedule."
        )

    elif consistency < 80:
        recommendations.append(
            "📈 Your consistency is improving. Aim for 80%+ consistency."
        )

    else:
        recommendations.append(
            "🔥 Excellent consistency! Keep following your study routine."
        )


    # ML prediction recommendation
    if predicted_score < 60:
        recommendations.append(
            "💪 Your predicted performance is low. "
            "Focus on consistency and completing more tasks."
        )

    elif predicted_score < 80:
        recommendations.append(
            "🎯 Your predicted performance is moderate. "
            "Increasing study time could help improve it."
        )

    else:
        recommendations.append(
            "🏆 Your predicted performance is strong. "
            "Focus on maintaining your current habits."
        )


    return recommendations