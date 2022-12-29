'''
useful functions for process data for dashboard
'''
import pandas as pd

from utility.read_data import read_portfolio_data, read_trading_data, read_current_position


def claculate_portfolio_value(first_trade_date='2020-01-09'):
    portfolio_value_df = read_portfolio_data()

    # only process portfolio data after first trade date
    portfolio_value_df = portfolio_value_df[portfolio_value_df.index >
                                            first_trade_date].copy()
    portfolio_value_df = portfolio_value_df[['portf_value', 'sp500_mktvalue',
                                             'ptf_value_pctch', 'sp500_pctch', 'ptf_value_diff', 'sp500_diff']].reset_index().round(2)

    # caluculate cumulative growth of portfolio after first trade date
    # change column name for chart
    portfolio_value_df.rename(columns={'index': 'date'}, inplace=True)
    portfolio_value_df.date = pd.to_datetime(portfolio_value_df.date)
    return portfolio_value_df


def calculate_invested_value():
    '''
    Net return of assets is calculated using column cash flow of the trades
    '''
    portfolio_value_df = claculate_portfolio_value()
    trading_df = read_trading_data()
    invested_value_df = (trading_df.groupby('date').sum()['cashflow']*-1)
    idx = pd.date_range(trading_df.date.min(), portfolio_value_df.date.max())
    invested_value_df = invested_value_df.reindex(
        idx, fill_value=0).reset_index()
    invested_value_df.rename(columns={'index': 'date'}, inplace=True)
    invested_value_df['total_cashflow'] = invested_value_df['cashflow'].cumsum()
    return invested_value_df


def calculate_chart_portfolio_value():
    portfolio_value_df = claculate_portfolio_value()
    invested_value_df = calculate_invested_value()
    chart_plotly_value_df = pd.merge(
        portfolio_value_df, invested_value_df, on='date', how='inner')
    # calculate the amount of money investd during the analysis period and store it in net_invested column
    chart_plotly_value_df['net_invested'] = chart_plotly_value_df['cashflow'].cumsum(
    )
    chart_plotly_value_df['net_value'] = chart_plotly_value_df['portf_value'] - \
        chart_plotly_value_df['net_invested']
    chart_plotly_value_df['ptf_growth'] = chart_plotly_value_df['net_value'] / \
        chart_plotly_value_df['net_value'].iloc[0]
    chart_plotly_value_df['sp500_growth'] = chart_plotly_value_df['sp500_mktvalue'] / \
        chart_plotly_value_df['sp500_mktvalue'].iloc[0]
    # accurate variation of investments is stored in column adjusted ptfchg
    chart_plotly_value_df['adjusted_ptfchg'] = (
        chart_plotly_value_df['net_value'].pct_change()*100).round(2)
    chart_plotly_value_df['highvalue'] = chart_plotly_value_df['net_value'].cummax(
    )
    chart_plotly_value_df['drawdownpct'] = (
        chart_plotly_value_df['net_value']/chart_plotly_value_df['highvalue']-1).round(4)*100

    return chart_plotly_value_df


def calculate_compare_growth():
    '''
    calculate dateframe for comparing portfolio growth and compare it with growth of S&P500
    '''
    portfolio_value_df = calculate_chart_portfolio_value()
    df = portfolio_value_df[['date', 'net_value', 'sp500_mktvalue']].copy()
    df['month'] = df.date.dt.month_name()
    df['weekday'] = df.date.dt.day_name()
    df['year'] = df.date.dt.year
    df['weeknumber'] = df.date.dt.isocalendar().week
    df['timeperiod'] = df.year.astype(
        str) + ' - ' + df.date.dt.month.astype(str).str.zfill(2)
    sp = df.reset_index().groupby('timeperiod').last()[
        'sp500_mktvalue'].pct_change()*100
    ptf = df.reset_index().groupby('timeperiod').last()[
        'net_value'].pct_change()*100
    growth_compare_df = pd.merge(ptf, sp, on='timeperiod').reset_index()

    return growth_compare_df


def calculate_datatable():
    current_position_df = read_current_position()
    current_position_df.columns = ['Ticker', 'Company', 'Sector', 'Industry', 'P/E', 'Perf Week', 'Perf Month', 'Perf Quart',
                                   'Perf Half', 'Perf Year', 'Perf YTD', 'Volatility Week', 'Volatility Month', 'Recom', 'ATR',
                                   'SMA20', 'SMA50', 'SMA200', '52W High', '52W Low', 'RSI', 'Insider Own', 'Insider Trans',
                                   'Inst Own', 'Inst Trans', 'Float Short', 'Short Ratio', 'Dividend', 'LTDebt/Eq', 'Debt/Eq',
                                   'Cumulative Units', 'Cumulative Cost ($)', 'Realized G/L ($)', 'Open Cashflow ($)',
                                   'Price ($)', 'Current Value ($)', 'Average Cost', 'Weight (%)', 'Unrealized ($)', 'Unrealized (%)']
    table_dict = {}
    for tick in current_position_df.Ticker:
        table = current_position_df[current_position_df.Ticker == tick].T.reset_index(
        )
        table.columns = ['indicator', tick]
        table_dict[tick] = table

    datatabletotal = current_position_df.to_dict('records')
    cols_total = [{"name": i, "id": i}
                  for i in current_position_df.columns[:10]]

    return datatabletotal, cols_total


def calculate_table_dict():
    current_position_df = read_current_position()
    current_position_df.columns = ['Ticker', 'Company', 'Sector', 'Industry', 'P/E', 'Perf Week', 'Perf Month', 'Perf Quart',
                                   'Perf Half', 'Perf Year', 'Perf YTD', 'Volatility Week', 'Volatility Month', 'Recom', 'ATR',
                                   'SMA20', 'SMA50', 'SMA200', '52W High', '52W Low', 'RSI', 'Insider Own', 'Insider Trans',
                                   'Inst Own', 'Inst Trans', 'Float Short', 'Short Ratio', 'Dividend', 'LTDebt/Eq', 'Debt/Eq',
                                   'Cumulative Units', 'Cumulative Cost ($)', 'Realized G/L ($)', 'Open Cashflow ($)',
                                   'Price ($)', 'Current Value ($)', 'Average Cost', 'Weight (%)', 'Unrealized ($)', 'Unrealized (%)']
    table_dict = {}
    for tick in current_position_df.Ticker:
        table = current_position_df[current_position_df.Ticker == tick].T.reset_index(
        )
        table.columns = ['indicator', tick]
        table_dict[tick] = table

    return table_dict
