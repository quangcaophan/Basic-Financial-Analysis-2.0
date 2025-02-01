from balance_sheet import *
from income_statement import *
from ratio import *
from cash_flow import *

import streamlit as st

# sidebar 
with st.sidebar:
    st.set_page_config(page_title="Stock Dashboard", layout="wide")
    st.title("Navigation")
    symbol = st.text_input('Enter your stock code here:', 'nvl').upper()
    page = st.sidebar.radio("Go to", ["Balance Sheet", "Income Statement","Cash Flow Statement","Ratio",'About'])

#get the data
balance_sheet           = get_balance_sheet(symbol,left_to_right=False) 
balance_sheet_left      = get_balance_sheet(symbol) 

income_statement        = get_income_statement(symbol)
cash_flow               = cash_flow_statement(symbol)
ratio                   = calculate_ratios(income_statement, balance_sheet_left)

horizontal_analysis_df  = horizontal_analysis(income_statement)
vertical_analysis_df    = vertical_analysis(income_statement) 


if page == "Balance Sheet":
    display_balance_sheet(balance_sheet_left,symbol)

elif page == "Income Statement":
    display_income_statement(income_statement, horizontal_analysis_df, vertical_analysis_df,symbol)

elif page == "Cash Flow Statement":
    display_cash_flow_statement(cash_flow,symbol)

elif page == "Ratio":
    display_ratio(ratio,symbol)

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

