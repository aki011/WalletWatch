# In utils.py
import plotly.express as px

def create_category_pie_chart(df):
    fig = px.pie(df, values='Amount', names='Category', title='Spending by Category')
    return fig
