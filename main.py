from balance_sheet import *
from income_statement import *
from ratio import *
from cash_flow import *
from Invest_over_a_period import *
from vnstock import Vnstock
import streamlit as st
from datetime import datetime

# sidebar 
with st.sidebar:
    st.set_page_config(page_title="Stock Dashboard", layout="wide")
    st.title("Navigation")
    symbol = st.text_input('Enter your stock code here:', 'nvl').upper()
    page = st.sidebar.radio("Go to", ["Balance Sheet", "Income Statement","Cash Flow Statement","Ratio","Invest Zone",'About'])

# Fetch stock data once
stock = Vnstock().stock(symbol=symbol, source='VCI')

#get the data
balance_sheet           = get_balance_sheet(fetch_balance_sheet(stock), left_to_right=False) 
balance_sheet_left      = get_balance_sheet(fetch_balance_sheet(stock))

income_statement        = get_income_statement(fetch_income_statement(stock))
cash_flow               = cash_flow_statement(fetch_cash_flow(stock))
ratio                   = calculate_ratios(income_statement, balance_sheet_left)

horizontal_analysis_df  = horizontal_analysis(income_statement)
vertical_analysis_df    = vertical_analysis(income_statement) 


if page == "Balance Sheet":
    st.write(f"Here's some information about the Balance Sheet: {symbol}")
    display_balance_sheet(balance_sheet_left,stock)

elif page == "Income Statement":
    st.write(f"Here's some information about the Income Statement for: {symbol}")
    display_income_statement(income_statement, horizontal_analysis_df, vertical_analysis_df,stock)

elif page == "Cash Flow Statement":
    st.write(f"Here's some information about the Cash Flow Statement: {symbol}")
    display_cash_flow_statement(cash_flow,stock)

elif page == "Invest Zone":
    st.write('Not available yet')

#     st.write(f"If you invest to {symbol} for a period of time, how much PnL you gonna make?")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         start_date = st.date_input("Start Date", datetime(2024, 1, 1))
#     with col2:
#         end_date = st.date_input("End Date", datetime(2024, 12, 31))
#     with col3:
#         daily_investment = st.number_input("Daily Investment (VND)", min_value=0, value=1000000)

#     start_date_str = start_date.strftime('%Y-%m-%d')
#     end_date_str = end_date.strftime('%Y-%m-%d')

#     invest = calculate_daily_investment_pnl(fetch_stock_history(stock, start_date_str, end_date_str), daily_investment=daily_investment)

#     st.write(f'Number of day: {end_date - start_date}')
#     st.write(invest)    

#     st.altair_chart(plot_pnl(invest), use_container_width=True)



    

elif page == "Ratio":
    display_ratio(ratio,stock)

elif page == "About":
    st.write("## FQA")

    with st.expander("How to read Ratio"):
        with open("About.md", "r") as f:
            about = f.read()
        st.markdown(about)

    with st.expander("How to read Horizontal Analysis"):
        st.write('''
            ### Horizontal Analysis (Time Series Analysis)
            - Horizontal Analysis, also known as Time Series Analysis, is a financial analysis technique that compares a business's financial data over multiple consecutive time periods.
            - It helps detect and evaluate trends, fluctuations and growth levels of financial indicators such as revenue, profit, total assets and liabilities over time.
        ''')

    with st.expander("How to read Vertical Analysis"):
        st.write("""
            ### Vertical Analysis (Common Size Analysis)
            - Vertical Analysis, also known as Common Size Analysis, is a financial analysis method that compares items in a financial statement with the total value of that financial statement.
            - This method is often used to determine the structure and distribution of income, expenses, assets and liabilities of a business. In this way, it allows to recognize the percentage of each item compared to the total value of the financial statement, helping to better understand the financial structure of the business.
            """)

