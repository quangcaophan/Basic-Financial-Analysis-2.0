import pandas as pd
import streamlit as st
import altair as alt


def fetch_income_statement(stock, year: int = 5):
    return stock.finance.income_statement(period='year', lang='vi', dropna=True).head(year)

@st.cache_data
def get_income_statement(income_statement: pd.DataFrame, left_to_right: bool = True) -> pd.DataFrame:
    """
    Get the income statement for the given symbol.
    Args:
        symbol (str): The stock symbol.
        year (int, optional): The number of years to retrieve. Defaults to 5.
        left_to_right (bool, optional): Whether to sort the income statement by year. Defaults to True.
    Returns:
        pd.DataFrame: The income statement for the given symbol.
    """
    if left_to_right == True:
        income_statement = income_statement.sort_values(by='Năm', ascending=True)
    income_statement = income_statement.transpose()
    income_statement.columns = income_statement.iloc[1]
    income_statement = income_statement.drop(income_statement.index[[0, 1]])

    return income_statement

def horizontal_analysis(income_statement: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the horizontal analysis for the given income statement data.
    Args:
        income_statement (pd.DataFrame): DataFrame containing income statement data.
    Returns:
        pd.DataFrame: A DataFrame with horizontal analysis values.
    """
    # Transpose the income statement
    income_statement = income_statement.transpose()
    income_statement = income_statement[['Doanh thu thuần', 'Lãi gộp', 'Lợi nhuận thuần']].transpose()

    # Calculate the horizontal analysis
    result_df = pd.DataFrame()
    for i in range(1, len(income_statement.columns)):
        result_df[income_statement.columns[i]] = round(((income_statement.iloc[:, i] / income_statement.iloc[:, 1]) - 1)*100)
    
    # Calculate CAGR
    num_years = len(income_statement.columns) - 1
    cagr = income_statement.apply(lambda row: ((row.iloc[-1] / row.iloc[0]) ** (1 / num_years) - 1) * 100 
                                  if row.iloc[-1] > 0 and row.iloc[0] > 0 else None, axis=1).round(2)
    result_df['CAGR'] = cagr
    
    return result_df

def vertical_analysis(income_statement: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the vertical analysis for the given income statement data.
    Args:
        income_statement (pd.DataFrame): DataFrame containing income statement data.
    Returns:
        pd.DataFrame: A DataFrame with coverage ratios.
    """
    # Transpose the income statement
    income_statement = income_statement.transpose()
    income_statement = income_statement[['Doanh thu thuần', 'Lãi gộp', 'Lợi nhuận thuần']].transpose()

    # Calculate the horizontal analysis
    result_df = pd.DataFrame()
    for col in income_statement.columns[1:]:
        result_df[col] = round((income_statement[col] / income_statement.iloc[0][col]) * 100)

    # Calculate CAGR
    num_years = len(income_statement.columns) - 1
    cagr = income_statement.apply(lambda row: ((row.iloc[-1] / row.iloc[0]) ** (1 / num_years) - 1) * 100 
                                  if row.iloc[-1] > 0 and row.iloc[0] > 0 else None, axis=1).round(2)
    result_df['CAGR'] = cagr    
    
    return result_df

def display_income_statement(
        income_statements: list,  # Đổi tên biến để rõ ràng hơn
        horizontal_analysis_df: pd.DataFrame, 
        vertical_analysis_df: pd.DataFrame, 
        symbols: list) -> None:
    """
    Display the income statement, analysis, and plot trends for the given symbols.
    
    Args:
        income_statements (list of DataFrame): List of income statements to plot.
        horizontal_analysis_df (pd.DataFrame): The horizontal analysis DataFrame.
        vertical_analysis_df (pd.DataFrame): The vertical analysis DataFrame.
        symbols (list): List of stock symbols.
        selected_columns (list of int): List of selected column indices.
    
    Returns:
        None
    """
    st.write(income_statements)
    with st.expander(f"Horizontal - Vertical Analysis"):
        col1, col2 = st.columns(2)
        with col1:
            # Horizontal Analysis
            st.write("## Horizontal Analysis")
            st.write(f"Horizontal Analysis for last {len(horizontal_analysis_df.columns) - 1} years")
            st.write(horizontal_analysis_df)

        with col2:
            # Vertical Analysis
            st.write("## Vertical Analysis")
            st.write(f"Vertical Analysis for last {len(vertical_analysis_df.columns) - 1} years")
            st.write(vertical_analysis_df)
        
        st.write(plot_trend_line(income_statements,symbols))
    
    with st.expander("WB Rule of Thumb for Income Statement"):
        st.write("### Gross Margin:")
        st.write('Not available yet')

        st.write("### SG&A Margin:")
        st.write('Not available yet')

        st.write("### R&D Margin:")
        st.write('Not available yet')

        st.write("### Depreciation Margin:")
        st.write('Not available yet')

        st.write("### Interest Margin:")
        st.write('Not available yet')

        st.write("### Tax Margin:")
        st.write('Not available yet')

        st.write("### Net Income Margin:")
        st.write('Not available yet')

        st.write("### EPS Margin:")
        st.write('Not available yet')

def plot_trend_line(income_statement, label):
    income_statement = income_statement.transpose()
    income_statement = income_statement[['Doanh thu thuần', 'Lãi gộp', 'Lợi nhuận thuần']]
    selected_columns = [0, 1, 2]  # Adjusted selected columns
    
    st.subheader(f"Trend Line")
    
    cols = st.columns(3)
    
    for i, cat_col in enumerate(income_statement.columns[selected_columns]):
        with cols[i]:
            st.write(f"**{cat_col}**")  # Hiển thị tên cột
            formatted_data = income_statement[cat_col] / 1e12  # Chuyển đổi sang nghìn tỷ
            
            df = pd.DataFrame({"Năm": pd.to_datetime(formatted_data.index, format='%Y'), "Value": formatted_data.values})
            min_value, max_value = df["Value"].min(), df["Value"].max()
            abs_max = max(abs(min_value), abs(max_value))  # Đảm bảo trục 0 ở giữa
            
            chart = (
                alt.Chart(df)
                .mark_line(point=True)
                .encode(x=alt.X("Năm:T", title="Năm"), y=alt.Y("Value:Q", scale=alt.Scale(domain=[-abs_max, abs_max])), tooltip=["Năm:T", "Value"])
            )
            
            st.altair_chart(chart, use_container_width=True)
            st.caption("Đơn vị: Nghìn tỷ")