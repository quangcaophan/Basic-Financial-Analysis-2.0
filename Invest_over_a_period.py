import altair as alt
import numpy as np
import streamlit as st
import pandas as pd

# def fetch_stock_history(stock, start_date, end_date):
#     """Fetch stock historical data."""
#     return stock.quote.history(start=start_date, end=end_date)

# @st.cache_data
# def calculate_daily_investment_pnl(stock_data: pd.DataFrame, daily_investment: float):
#     """Calculate daily investment PnL."""
#     data = stock_data.copy()
#     data['shares_bought'] = daily_investment / data['close']
#     data['total_shares'] = data['shares_bought'].cumsum()
#     data['total_investment'] = daily_investment * np.arange(len(data))
#     data['portfolio_value'] = data['total_shares'] * data['close']
#     data['PnL'] = data['portfolio_value'] - data['total_investment']
    
#     return data

# def plot_pnl(data):
#     """Plot PnL growth over time."""
#     chart = alt.Chart(data.reset_index()).mark_line(color='blue').encode(
#         x='time:T',
#         y='PnL:Q'
#     ).properties(
#         title='PnL Growth Over Time'
#     )
#     return chart
# # ---------------------------------------------------------------

def fetch_stock_history(stock, start_date, end_date):
    df = stock.quote.history(start=start_date, end=end_date, interval='1D')
    return df 


def get_data(df, date_type):
    df = df[['time', 'open']].copy()  # Chỉ giữ cột cần thiết để tăng tốc
    df['time'] = pd.to_datetime(df['time'])
    df = df.drop_duplicates(subset=['time'], keep='first')

    if date_type == 'Day':
        return df.sort_values(by='time', ascending=True)

    elif date_type == 'Month':
        df['date_type'] = df['time'].dt.to_period('M')
        price_by_month = df.groupby('date_type').first().reset_index()
        return price_by_month[['time','open']].sort_values(by='time', ascending=True)
    
    elif date_type == 'Year':
        df['date_type'] = df['time'].dt.to_period('Y')
        price_by_year = df.groupby('date_type').first().reset_index()
        return price_by_year[['time','open']].sort_values(by='time',ascending=True)
    
    return df



def calculate_dca(df, investment):
    df = df.copy()
    df['Quantity'] = (investment / df['open']).round()
    df['Total Quantity'] = df['Quantity'].cumsum().round()
    df['Total Cost'] = ((df.index + 1) * investment)
    df['Current Value'] = (df['Total Quantity'] * df['open']).round()
    df['PnL'] = (df['Current Value'] - df['Total Cost']).round()
    return df[['time', 'open', 'Quantity', 'Total Quantity','Total Cost', 'Current Value', 'PnL']]



def plot_pnl_chart(dca_df):
    dca_df = dca_df.copy()
    dca_df['time'] = pd.to_datetime(dca_df['time'])
    
    chart = alt.Chart(dca_df).mark_line().encode(
        x=alt.X('time:T', title='Date'),
        y=alt.Y('PnL:Q', title='Profit & Loss'),
        tooltip=['time', 'PnL']
    ).properties(
        title='PnL Over Time'
    )
    return chart
