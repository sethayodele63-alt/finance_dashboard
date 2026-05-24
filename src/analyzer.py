import pandas as pd

def monthly_summary(df):
    """Total spending per category per month"""
    return df.groupby(["month", "category"])["amount"].sum().reset_index()

def top_merchants(df, n=5):
    """Top N merchants by total spend"""
    return df.groupby("merchant")["amount"].sum().nlargest(n).reset_index()

def monthly_totals(df):
    """Total spend per month"""
    return df.groupby("month")["amount"].sum().reset_index()

def category_totals(df):
    """Total spend per category across all time"""
    return df.groupby("category")["amount"].sum().reset_index()

def detect_anomalies(df):
    """Flag transactions 2x above the merchant's average"""
    merchant_avg = df.groupby("merchant")["amount"].mean()
    df = df.copy()
    df["merchant_avg"] = df["merchant"].map(merchant_avg)
    df["is_anomaly"] = df["amount"] > (df["merchant_avg"] * 2)
    return df[df["is_anomaly"]][["date", "merchant", "amount", "category", "merchant_avg"]]

def budget_status(df, budgets):
    """Compare actual spending vs user-defined budgets per category"""
    actual = df.groupby("category")["amount"].sum().reset_index()
    actual.columns = ["category", "actual"]
    results = []
    for _, row in actual.iterrows():
        budget = budgets.get(row["category"], None)
        if budget:
            results.append({
                "category": row["category"],
                "actual": row["actual"],
                "budget": budget,
                "difference": budget - row["actual"],
                "status": "✅ Under" if row["actual"] <= budget else "⚠️ Over"
            })
    return pd.DataFrame(results)