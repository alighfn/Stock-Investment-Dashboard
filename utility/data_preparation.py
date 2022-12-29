'''
useful functions for preparing data for dashboard
'''

import pandas as pd
from datetime import datetime


def clean_header(df):
    df.columns = df.columns.str.strip().str.lower().str.replace('.', '', regex=False).str.replace('(',
                                                                                                  '', regex=False).str.replace(')', '', regex=False).str.replace(' ', '_', regex=False).str.replace('_/_', '/', regex=False)


def get_now():
    now = datetime.now().strftime('%Y-%m-%d_%Hh%Mm')
    return now


def datetime_maker(df, datecol):
    df[datecol] = pd.to_datetime(df[datecol])


def date_parser(x):
    return pd.datetime.strptime(x, "%m/%d/%Y")
