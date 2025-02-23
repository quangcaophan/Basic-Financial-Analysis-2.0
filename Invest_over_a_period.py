import altair as alt
import numpy as np
import streamlit as st
import pandas as pd

def fetch_stock_history(stock, start_date, end_date):
    """Fetch stock historical data."""
    return stock.quote.history(start=start_date, end=end_date)

@st.cache_data
def calculate_daily_investment_pnl(stock_data: pd.DataFrame, daily_investment: float):
    """Calculate daily investment PnL."""
    data = stock_data.copy()
    data['shares_bought'] = daily_investment / data['close']
    data['total_shares'] = data['shares_bought'].cumsum()
    data['total_investment'] = daily_investment * np.arange(len(data))
    data['portfolio_value'] = data['total_shares'] * data['close']
    data['PnL'] = data['portfolio_value'] - data['total_investment']
    
    return data

def plot_pnl(data):
    """Plot PnL growth over time."""
    chart = alt.Chart(data.reset_index()).mark_line(color='blue').encode(
        x='time:T',
        y='PnL:Q'
    ).properties(
        title='PnL Growth Over Time'
    )
    return chart
