'''
useful functions for reading data for dashboard
'''
import pandas as pd
import yfinance as yf

from utility.data_preparation import date_parser


def read_trading_data(path='data\\trading_data.xlsx'):

    trading_df = pd.read_excel(path)
    trading_df.date = pd.to_datetime(
        trading_df.date, format='%d/%m/%Y')
    return trading_df


def read_portfolio_data(path='data\\portfolio.xlsx'):

    portfolio_df = pd.read_excel(path, index_col='date', parse_dates=[
                                 'date'])
    portfolio_df.index = pd.to_datetime(portfolio_df.index, format='%d/%m/%Y')

    # portfolio_df.date = pd.to_datetime(portfolio_df.date, format='%d/%m/%Y')
    return portfolio_df


def read_current_position(path='data\\current_positions.xlsx'):
    position_df = pd.read_excel(path)
    position_df = position_df.sort_values(
        by='current_value', ascending=False).round(2)
    return position_df


def read_ohlcv(ticker_name, start_date='2020-01-01', end_date='2021-12-31'):
    '''
    read ohlcv data of a ticker from start date to end date
    '''
    print(f'Fetching {ticker_name} OHLCV data from Yahoo Finance...')
    ohlcv_df = yf.download(ticker_name, start=start_date, end=end_date)
    ohlcv_df.rename(columns={'Open': 'open', 'High': 'high',
                             'Low': 'low', 'Close': 'close', 'Volume': "volume"}, inplace=True)
    ohlcv_df['date'] = ohlcv_df.index

    return ohlcv_df
