import pandas as pd
import streamlit as st
from income_statement import get_income_statement
from balance_sheet import get_balance_sheet


def calculate_ratios(symbol: str) -> pd.DataFrame:
    """
    Calculate the financial ratios for the given balance sheet data.
    Args:
        symbol (str): The stock symbol.
    Returns:
        pd.DataFrame: A DataFrame with financial ratios.
    """    
    # Get the data
    balance_sheet           = get_balance_sheet(symbol).transpose()
    income_statement        = get_income_statement(symbol).transpose()
    
    # Extract the necessary data
    total_asset             = balance_sheet['TỔNG CỘNG TÀI SẢN (Tỷ đồng)']
    total_liabilities       = balance_sheet['NỢ PHẢI TRẢ (Tỷ đồng)']
    inventory               = balance_sheet['Hàng tồn kho ròng']
    current_asset           = balance_sheet['TÀI SẢN NGẮN HẠN (Tỷ đồng)']
    cash_equivalents        = balance_sheet['Tiền và tương đương tiền (Tỷ đồng)']
    short_term_debt         = balance_sheet['Nợ ngắn hạn (Tỷ đồng)']
    short_term_investment   = balance_sheet['Giá trị thuần đầu tư ngắn hạn (Tỷ đồng)']
    total_equity            = balance_sheet['VỐN CHỦ SỞ HỮU (Tỷ đồng)']
    
    net_income              = income_statement['Lợi nhuận thuần'] 

    # Calculate the Liquidity Ratios
    current_ratio           = round(total_asset / total_liabilities,2)
    quick_ratio             = round((current_asset - inventory) / short_term_debt,2)
    cash_ratio              = round((cash_equivalents + short_term_investment) / short_term_debt,2)

    # Calculate the Solvency Ratios
    debt_to_asset_ratio     = round(total_liabilities / total_asset,2)
    debt_to_equity_ratio    = round(total_liabilities / total_equity,2)
    equity_ratio            = round(total_equity / total_asset,2)

    # Create a Dataframe to store Solvency and Liquidity data
    liquidity_solvency_df = pd.DataFrame({
        'Khả năng thanh toán tổng quát': round(current_ratio,2),
        'Khả năng thanh toán nhanh': round(quick_ratio,2),
        'Khả năng thanh toán tức thời': round(cash_ratio,2),
        'D/A': round(debt_to_asset_ratio,2),
        'E/A': round(equity_ratio,2),
        'D/E': round(debt_to_equity_ratio,2)
    }).transpose()


    # Calculalte ROA and ROE
    balance_df              = balance_sheet[['TỔNG CỘNG TÀI SẢN (Tỷ đồng)', 'VỐN CHỦ SỞ HỮU (Tỷ đồng)']].transpose()
    income_df               = income_statement[['Lợi nhuận thuần']].transpose()

    profitability_df = pd.DataFrame()

    for i in range(0, len(income_df.columns) - 1):
        year                = income_df.columns[i + 1]  # Lấy năm làm index
        # Store Net Income and Assets
        net_income          = income_df.iloc[-1, i + 1]
        first_assets        = balance_df.iloc[0, i]
        second_assets       = balance_df.iloc[0, i + 1]

        # Store EquityEquity
        first_equity        = balance_df.iloc[-1, i]
        second_equity       = balance_df.iloc[-1, i + 1]

        # Calculate the ratios
        ROA = net_income / ((first_assets + second_assets) / 2) * 100
        ROE = net_income / ((first_equity + second_equity) / 2) * 100

        profitability_df[year] = pd.Series({
            'ROE': round(ROE,2),
            'ROA': round(ROA,2) 
        })
    

    # Calculate efficienty ratio
    income_df               = income_statement[['Doanh thu thuần']].transpose()
    balance_df              = balance_sheet[['TỔNG CỘNG TÀI SẢN (Tỷ đồng)','Hàng tồn kho ròng']].transpose()

    efficienty_ratio_df = pd.DataFrame()

    for i in range(0, len(income_df.columns) - 1):
        year                = income_df.columns[i + 1]  # Lấy năm làm index
        # Store Total Sales and Assets
        sales               = income_df.iloc[0, i + 1]
        first_assets        = balance_df.iloc[0, i]
        second_assets       = balance_df.iloc[0, i + 1]

        # Store COGS and Inventory
        inventory           = balance_df.iloc[1, i + 1]
        first_inventory     = balance_df.iloc[1, i]
        second_inventory    = balance_df.iloc[1, i + 1]

        # Calculate the ratios
        atr = sales / ((first_assets + second_assets) / 2)
        itr = inventory / ((first_inventory + second_inventory) / 2)

        # Store the ratios in the result dataframe
        efficienty_ratio_df[year] = pd.Series({
            'ATR': round(atr,2),
            'ITR': round(itr,2)
        })

    # Merge 2 dataset
    final_result_df = pd.concat([
        liquidity_solvency_df, 
        profitability_df,
        efficienty_ratio_df
    ], axis=0)
    final_result_df.index.name = 'Năm'

    return final_result_df


def display_ratio(ratio: pd.DataFrame, symbol: str) -> None:
    """
    Display the ratios for the given symbol.
    Args:
        ratio (pd.DataFrame): The ratios DataFrame.
        symbol (str): The stock symbol.
    """
    st.write(f"Here's some information about the Ratio for: {symbol}")
    ratio['Historical data'] = ratio.iloc[:, 1:].apply(lambda x: x.tolist(), axis=1)
    st.data_editor(
        ratio,
        column_config={
            "Historical data": st.column_config.AreaChartColumn(
                "Historical data",
                width="medium",
                help=f"The ratio past {len(ratio.columns)-1} years"
            ),
        },
    )