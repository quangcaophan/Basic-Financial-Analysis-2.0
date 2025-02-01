import pandas as pd
from vnstock import Vnstock
import streamlit as st

@st.cache_data
def cash_flow_statement(symbol: str, year: int = 5, left_to_right: bool = True) -> pd.DataFrame:
    """
    Get the cash flow statement for the given symbol.
    Args:
        symbol (str): The stock symbol.
        year (int, optional): The number of years to retrieve. Defaults to 5.
        left_to_right (bool, optional): Whether to sort the cash flow statement by year. Defaults to True.
    Returns:
        pd.DataFrame: The cash flow statement for the given symbol.
    """
    stock = Vnstock().stock(symbol=symbol, source='VCI')
    cashflow_statement = stock.finance.cash_flow(period='year', lang='vi', dropna=True).head(year)
    if left_to_right == True:
        cashflow_statement = cashflow_statement.sort_values(by='Năm', ascending=True)
    cashflow_statement = cashflow_statement.transpose()
    cashflow_statement.columns = cashflow_statement.iloc[1]  # Set the first row as header
    cashflow_statement = cashflow_statement.drop(cashflow_statement.index[[0, 1]])
    
    return cashflow_statement

@st.cache_data
def display_cash_flow_statement(cashflow_statement: pd.DataFrame, symbol: str) -> None:
    """
    Display the cash flow statement for the given symbol.
    Args:
        cashflow_statement (pd.DataFrame): The cash flow statement DataFrame.
        symbol (str): The stock symbol.
    Returns:
        None
    """
    st.write(f"## Here's some information about the Cash Flow Statement: {symbol}")
    st.write(cashflow_statement)
    with st.expander("WB Rule of Thumb for Cash Flow Statement"):
        st.write("### Capex Margin:")
        st.write('Not available yet')