def get_recommendations(df, budgets=None):
    """Generate simple savings recommendations based on spending patterns"""
    recommendations = []

    total_spend = df["amount"].sum()
    category_totals = df.groupby("category")["amount"].sum()

    # Check food & dining
    food_spend = category_totals.get("Food & Dining", 0)
    food_pct = (food_spend / total_spend) * 100
    if food_pct > 25:
        recommendations.append(
            f"🍔 You spent {food_pct:.1f}% of your money on Food & Dining. "
            f"Try to keep this under 25%. You could save ₦{food_spend * 0.2:,.0f} by cutting back 20%."
        )

    # Check entertainment
    entertainment_spend = category_totals.get("Entertainment", 0)
    entertainment_pct = (entertainment_spend / total_spend) * 100
    if entertainment_pct > 10:
        recommendations.append(
            f"🎬 Entertainment is {entertainment_pct:.1f}% of your spend. "
            f"Consider reducing subscriptions to save ₦{entertainment_spend * 0.3:,.0f} monthly."
        )

    # Check transport
    transport_spend = category_totals.get("Transport", 0)
    transport_pct = (transport_spend / total_spend) * 100
    if transport_pct > 20:
        recommendations.append(
            f"🚗 Transport is eating {transport_pct:.1f}% of your budget. "
            f"Carpooling or public transport could save you ₦{transport_spend * 0.25:,.0f}."
        )

    # Check cash withdrawals
    cash_spend = category_totals.get("Cash Withdrawal", 0)
    cash_pct = (cash_spend / total_spend) * 100
    if cash_pct > 15:
        recommendations.append(
            f"💵 {cash_pct:.1f}% of spending is cash withdrawals — hard to track! "
            f"Try paying digitally to monitor your spending better."
        )

    # Check budget overruns
    if budgets:
        for category, budget in budgets.items():
            actual = category_totals.get(category, 0)
            if actual > budget:
                recommendations.append(
                    f"🚨 You exceeded your {category} budget by ₦{actual - budget:,.0f}!"
                )

    if not recommendations:
        recommendations.append("🎉 Great job! Your spending looks healthy across all categories.")

    return recommendations