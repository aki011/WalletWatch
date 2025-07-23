def recommend(df, monthly_income):
    recommendations = []

    avg_spend = df['Amount'].mean()
    max_spend = df['Amount'].max()
    total_spend = df['Amount'].sum()
    food_count = df['Category'].value_counts().get("Food", 0)
    travel_count = df['Category'].value_counts().get("Travel", 0)
    shopping_count = df['Category'].value_counts().get("Shopping", 0)

    # Budgeting tips
    if avg_spend > (0.5 * monthly_income):
        recommendations.append("⚠️ Your average monthly spending exceeds 50% of your income. Consider budgeting tightly.")

    if total_spend > (monthly_income * 3):
        recommendations.append("📊 Your total spending is 3x more than your income. Time for a detailed review!")

    # Specific category feedback
    if food_count > 10:
        recommendations.append("🍕 High food expenses detected. Cooking at home might help reduce costs.")
    if travel_count > 5:
        recommendations.append("✈️ You’ve been spending a lot on travel. Plan your trips more economically.")
    if shopping_count > 5:
        recommendations.append("🛍️ Frequent shopping detected. Consider tracking wants vs. needs.")

    # Outlier transaction
    if max_spend > (0.75 * monthly_income):
        recommendations.append(f"💸 One of your transactions was ₹{int(max_spend)}. Consider reviewing that purchase.")

    # Generic advice
    if not recommendations:
        recommendations.append("🎉 Great job! Your spending seems balanced. Keep it up!")

    return recommendations
