import pandas as pd
import numpy as np
import random
import os

def generate_sample_data():
    random.seed(42)
    
    merchants = [
        "Shoprite", "Uber", "DSTV", "GTBank ATM",
        "Jumia", "Bolt", "MTN Airtime", "Shell Station",
        "Chicken Republic", "Netflix", "Konga", "Total Filling Station",
        "Dominos Pizza", "Paystack", "Flutterwave", "Zenith Bank ATM"
    ]

    categories = [
        "Groceries", "Transport", "Entertainment", "Cash Withdrawal",
        "Shopping", "Transport", "Airtime & Data", "Fuel",
        "Food & Dining", "Entertainment", "Shopping", "Fuel",
        "Food & Dining", "Business", "Business", "Cash Withdrawal"
    ]

    rows = []
    for _ in range(200):
        i = random.randint(0, len(merchants) - 1)
        rows.append({
            "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=random.randint(0, 180)),
            "merchant": merchants[i],
            "amount": round(random.uniform(500, 25000), 2),
            "category": categories[i]
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("date").reset_index(drop=True)

    os.makedirs("data", exist_ok=True)
    df.to_csv("data/transactions.csv", index=False)
    print("✅ Sample data generated: data/transactions.csv")
    return df

def load_data(filepath="data/transactions.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    df["week"] = df["date"].dt.isocalendar().week
    return df