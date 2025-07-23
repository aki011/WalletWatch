import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def monthly_trend_plot(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly = df.groupby('Month')['Amount'].sum().reset_index()

    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly, x='Month', y='Amount', marker='o')
    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Spent (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt
