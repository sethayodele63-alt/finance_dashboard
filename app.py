import streamlit as st
import plotly.express as px
from src.loader import load_data, generate_sample_data
from src.analyzer import (
    monthly_summary, top_merchants, monthly_totals,
    category_totals, detect_anomalies, budget_status
)
from src.recommender import get_recommendations
import os

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Finance Dashboard",
    page_icon="💳",
    layout="wide"
)

# ── Generate data if it doesn't exist ────────────────────────
if not os.path.exists("data/transactions.csv"):
    generate_sample_data()

# ── Load data ─────────────────────────────────────────────────
df = load_data()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.title("💳 Finance Dashboard")
st.sidebar.markdown("---")

months = ["All"] + sorted(df["month"].unique().tolist())
selected_month = st.sidebar.selectbox("📅 Filter by Month", months)

st.sidebar.markdown("### 🎯 Set Monthly Budgets (₦)")
categories = df["category"].unique().tolist()
budgets = {}
for cat in categories:
    budgets[cat] = st.sidebar.number_input(f"{cat}", min_value=0, value=50000, step=5000)

# ── Filter data ───────────────────────────────────────────────
filtered_df = df if selected_month == "All" else df[df["month"] == selected_month]

# ── Header ────────────────────────────────────────────────────
st.title("💳 Personal Finance Dashboard")
st.markdown("Track your spending, spot anomalies, and save more money.")
st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Spend", f"₦{filtered_df['amount'].sum():,.0f}")
col2.metric("🧾 Transactions", len(filtered_df))
col3.metric("📊 Avg Transaction", f"₦{filtered_df['amount'].mean():,.0f}")
col4.metric("🏪 Unique Merchants", filtered_df["merchant"].nunique())

st.markdown("---")

# ── Charts Row 1 ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Spend by Category")
    cat_data = category_totals(filtered_df)
    fig = px.bar(cat_data, x="category", y="amount",
                 color="category", text_auto=True,
                 labels={"amount": "Amount (₦)", "category": "Category"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🥧 Share of Wallet")
    fig2 = px.pie(cat_data, names="category", values="amount", hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Monthly Spending Trend")
    monthly = monthly_totals(df)
    fig3 = px.line(monthly, x="month", y="amount", markers=True,
                   labels={"amount": "Amount (₦)", "month": "Month"})
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🏪 Top 5 Merchants")
    top = top_merchants(filtered_df)
    fig4 = px.bar(top, x="amount", y="merchant", orientation="h",
                  color="amount", text_auto=True,
                  labels={"amount": "Amount (₦)", "merchant": "Merchant"})
    fig4.update_layout(showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# ── Budget Status ─────────────────────────────────────────────
st.markdown("---")
st.subheader("🎯 Budget vs Actual")
budget_df = budget_status(filtered_df, budgets)
if not budget_df.empty:
    for _, row in budget_df.iterrows():
        color = "🟢" if row["status"] == "✅ Under" else "🔴"
        st.markdown(
            f"{color} **{row['category']}** — "
            f"Spent: ₦{row['actual']:,.0f} | Budget: ₦{row['budget']:,.0f} | "
            f"{row['status']} by ₦{abs(row['difference']):,.0f}"
        )

# ── Anomalies ─────────────────────────────────────────────────
st.markdown("---")
st.subheader("🚨 Unusual Transactions")
anomalies = detect_anomalies(filtered_df)
if anomalies.empty:
    st.success("No unusual transactions detected!")
else:
    st.dataframe(anomalies, use_container_width=True)

# ── Recommendations ───────────────────────────────────────────
st.markdown("---")
st.subheader("💡 Savings Recommendations")
tips = get_recommendations(filtered_df, budgets)
for tip in tips:
    st.info(tip)

# ── Raw Data ──────────────────────────────────────────────────
st.markdown("---")
with st.expander("🗂 View Raw Transactions"):
    st.dataframe(filtered_df, use_container_width=True)