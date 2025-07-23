import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
import os

# Custom imports
from utils import create_category_pie_chart
from insights import monthly_trend_plot
from model import cluster_spending
from recommender import recommend
import preprocess  # Modified import to avoid circular import issue

# Set Streamlit page config
st.set_page_config(page_title="FinSight", layout="wide")

# ----------------------------
# Sidebar Personalization
# ----------------------------
st.sidebar.image("assets/logo.png", width=80)
st.sidebar.title("🔍 Personal Finance Tracker")
st.sidebar.markdown("Upload your expenses & get insights")

user_name = st.sidebar.text_input("👤 Enter your name", "Akshay")
st.sidebar.markdown(f"Welcome, **{user_name}**! 🎉")

# ----------------------------
# Monthly Income Input
# ----------------------------
monthly_income = st.sidebar.number_input("💼 Enter your Monthly Income (₹)", min_value=0, value=30000, step=1000)

# ----------------------------
# File Upload Handling
# ----------------------------
uploaded_file = st.sidebar.file_uploader("📤 Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        cleaned_df = preprocess.preprocess_uploaded_file(uploaded_file)  # Updated function call
        cleaned_df.to_csv("data/cleaned_expense_data.csv", index=False)
        st.sidebar.success("✅ File uploaded and processed!")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to process file: {e}")

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    if os.path.exists("data/cleaned_expense_data.csv"):
        return pd.read_csv("data/cleaned_expense_data.csv", parse_dates=["Date"])
    else:
        return pd.DataFrame()

df = load_data()

# ----------------------------
# Tabs Setup
# ----------------------------
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📈 ML Insights", "💡 Recommendations"])

# ----------------------------
# Dashboard Tab
# ----------------------------
with tab1:
    col1, col2 = st.columns([2,15])
    with col1:
        st.image("assets/logo.png", width=100)
    with col2:
        st.title("WalletWatch - Personal Finance Tracker")

    if df.empty:
        st.info("📥 Please upload a CSV file to view insights.")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="💰 Total Spent", value="₹0.00")
        col2.metric(label="📈 Avg. Transaction", value="₹0.00")
        col3.metric(label="💸 Estimated Savings", value=f"₹{monthly_income:,.2f}")
    else:
        # Date filtering
        st.subheader("📅 Filter by Date")
        min_date = df['Date'].min()
        max_date = df['Date'].max()
        start_date, end_date = st.date_input("Select date range:", [min_date, max_date])

        filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        with st.expander("📋 View Filtered Transactions"):
            st.dataframe(filtered_df, use_container_width=True)

        # Expenses
        total_expense = filtered_df['Amount'].sum()
        avg_spend = filtered_df['Amount'].mean() if not filtered_df.empty else 0
        savings = monthly_income - total_expense

        col1, col2, col3 = st.columns(3)
        col1.metric(label="💰 Total Spent", value=f"₹{total_expense:,.2f}")
        col2.metric(label="📈 Avg. Transaction", value=f"₹{avg_spend:,.2f}")
        col3.metric(label="💸 Estimated Savings", value=f"₹{savings:,.2f}",
                    delta=f"{'🔺 Good' if savings > 0 else '🔻 Overspending'}")

        # Pie Chart
        with st.expander("📊 Category-wise Distribution"):
            st.plotly_chart(create_category_pie_chart(filtered_df), use_container_width=True)

        # Bar Chart
        with st.expander("📁 Category-wise Expenses"):
            category_df = filtered_df.groupby('Category', as_index=False)['Amount'].sum()
            fig, ax = plt.subplots()
            sns.barplot(data=category_df, x='Category', y='Amount', ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        # Monthly trend
        st.subheader("📆 Monthly Spending Trend")
        st.pyplot(monthly_trend_plot(filtered_df))

# ----------------------------
# ML Insights Tab
# ----------------------------
with tab2:
    st.subheader("🔍 Spending Pattern Clusters")
    if df.empty:
        st.info("📥 Upload a CSV to see ML insights.")
    else:
        clusters = cluster_spending(df)
        st.dataframe(clusters, use_container_width=True)

        with st.expander("📌 Cluster Summary"):
            cluster_summary = clusters.groupby('Cluster')['Amount'].agg(['mean', 'sum', 'count']).reset_index()
            st.dataframe(cluster_summary)

# ----------------------------
# Recommendations Tab
# ----------------------------
with tab3:
    st.subheader("🧠 Smart Recommendations")
    if df.empty:
        st.info("📥 Upload a CSV to get recommendations.")
    else:
        tips = recommend(df, monthly_income)

        for tip in tips:
            if "⚠️" in tip or "💸" in tip:
                st.warning(tip)
            elif "📊" in tip or "✈️" in tip:
                st.info(tip)
            elif "🎉" in tip:
                st.success(tip)
            else:
                st.markdown(f"- {tip}")

        with st.expander("💰 Savings Overview"):
            total_expense = df['Amount'].sum()
            savings = monthly_income - total_expense
            savings_percentage = max(0, (savings / monthly_income) * 100)

            st.metric("Savings %", f"{savings_percentage:.1f}%")
            st.progress(min(int(savings_percentage), 100))

        st.markdown("---")
        st.markdown("### 📌 More Personalized Suggestions:")
        st.warning("🔍 Review your top 3 spending categories and consider setting monthly limits.")
        st.success("📥 Track subscriptions or recurring expenses to cut unnecessary costs.")
        st.info("📊 Use the ML Clusters tab to identify if you belong to a high-spending group and take corrective steps.")
        st.warning("🎯 Set savings goals and track them using monthly comparisons.")


# ----------------------------
# Sidebar Summary
# ----------------------------
with st.sidebar:
    st.markdown("---")
    if df.empty:
        st.metric("📅 This Month's Spend", "₹0")
        st.metric("💸 Estimated Savings", f"₹{monthly_income:,.0f}")
        st.metric("📊 Total Spent", "₹0")
        st.info("Upload data to see summaries and charts.")
    else:
        # Ensure Date column is in datetime format
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True)

        # Ensure Month column exists
        if 'Month' not in df.columns:
            df['Month'] = df['Date'].dt.to_period('M').astype(str)

        current_month = pd.Timestamp.today().to_period("M").strftime("%Y-%m")
        this_month_df = df[df['Month'] == current_month]
        this_month_total = this_month_df['Amount'].sum()

        total_spent = df['Amount'].sum()
        estimated_savings = monthly_income - this_month_total

        st.metric("📅 This Month's Spend", f"₹{this_month_total:,.0f}")
        st.metric("💸 Estimated Savings", f"₹{estimated_savings:,.0f}")
        st.metric("📊 Total Spent", f"₹{total_spent:,.0f}")

        st.markdown("---")
        st.markdown("🔄 **Quick Tips:**")
        st.success("Use the date filter to analyze specific periods.")
        st.info("Try uploading next month's expenses to compare trends.")
