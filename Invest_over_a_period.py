import altair as alt
import pandas as pd

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

    # Biểu đồ Current ValuePnL
    pnl_chart = alt.Chart(dca_df).mark_line(color='blue').encode(
        x=alt.X('time:T', title='Date'),
        y=alt.Y('Current Value:Q', title='Current Value'),
        tooltip=['time', 'Current Value']
    )

    # Biểu đồ Current Value (được vẽ phía sau)
    value_chart = alt.Chart(dca_df).mark_line(color='red').encode(
        x=alt.X('time:T', title='Date'),
        y=alt.Y('Total Cost:Q', title='Total Cost'),
        tooltip=['time', 'Total Cost']
    )

    # Kết hợp hai biểu đồ
    final_chart = alt.layer(value_chart, pnl_chart).properties(title='Current Value & Total Cost Over Time')

    return final_chart

