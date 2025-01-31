import pandas as pd
from vnstock import Vnstock
import streamlit as st

def get_balance_sheet(symbol: str, year: int = 5,left_to_right: bool = True) -> pd.DataFrame:
    """
    Get the balance sheet for the given symbol.
    Args:
        symbol (str): The stock symbol.
        year (int, optional): The number of years to include in the balance sheet. Defaults to 5.
        left_to_right (bool, optional): Whether to sort the balance sheet by year. Defaults to True.
    Returns:
        pd.DataFrame: The balance sheet DataFrame.
    """
    stock = Vnstock().stock(symbol=symbol, source='VCI')
    balance_sheet = stock.finance.balance_sheet(period='year', lang='vi', dropna=True).head(year)
    if left_to_right == True:
        balance_sheet = balance_sheet.sort_values(by='Năm', ascending=True)
    balance_sheet = balance_sheet.transpose()
    balance_sheet.columns = balance_sheet.iloc[1]  # Set the first row as header
    balance_sheet = balance_sheet.drop(balance_sheet.index[[0, 1]])
    
    return balance_sheet

def display_balance_sheet(balance_sheet: pd.DataFrame, symbol) -> None:
    """ 
    Display the balance sheet for the given symbol.
    Args:
        balance_sheet (pd.DataFrame): The balance sheet DataFrame.
        symbol (str): The stock symbol.
    """
    st.write(f"Here's some information about the Balance Sheet: {symbol}")
    st.write(balance_sheet)
    
    balance_sheet = balance_sheet.transpose().head(1)

    with st.expander("WB Rule of Thumb for Balance Sheet"):
        # Cash & Debt
        st.write("### Cash & Debt:")
        st.write(balance_sheet[['Tiền và tương đương tiền (Tỷ đồng)','NỢ PHẢI TRẢ (Tỷ đồng)']]/1000000000)
        if balance_sheet['Tiền và tương đương tiền (Tỷ đồng)'].iloc[0] > balance_sheet['NỢ PHẢI TRẢ (Tỷ đồng)'].iloc[0]:
            st.success('The amount of cash is greater than the amount of debt.')
        else:
            st.warning('The amount of cash is less than the amount of debt.')

        # Adjusted Debt to Equity
        st.write("### Adjusted Debt to Equity:")
        result = balance_sheet['NỢ PHẢI TRẢ (Tỷ đồng)'].iloc[0] / balance_sheet['VỐN CHỦ SỞ HỮU (Tỷ đồng)'].iloc[0]
        st.write(f'Adjusted Debt to Equity: {round(result,2)}')
        if result < 0.8:
            st.success('The adjusted debt to equity ratio is less than 0.8.')
        else:
            st.warning('The adjusted debt to equity ratio is greater than 0.8.')

        # Preferred Stock
        st.write("### Preferred Stock:")
        if 'Cổ phiếu ưu đãi' not in balance_sheet.columns:
            st.success('There is no preferred stock.')
        elif balance_sheet['Cổ phiếu ưu đãi (Tỷ đồng)'].iloc[0] == 0:
            st.success('There is no preferred stock.')
        else:
            st.warning('There is preferred stock.')

        # Treasury Stock
        st.write("### Treasury Stock:")
        if 'Cổ phiếu quỹ' not in balance_sheet.columns:
            st.success('There is no Treasury Stock.')
        elif balance_sheet['Cổ phiếu ưu đãi (Tỷ đồng)'].iloc[0] == 0:
            st.success('There is no Treasury Stock.')
        else:
            st.warning('There is Treasury Stock.')
