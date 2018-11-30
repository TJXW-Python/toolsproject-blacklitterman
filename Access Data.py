################### This should not be run if user does not want to update the pool of assets!!! ###################

from pandas import *

from datetime import datetime
# terminal: $ pip install pandas-datareader
# or conda install -c anaconda pandas-datareader 
import pandas_datareader as pdr


# Functions download data given a file for stock symbols

base = 'data/'
def write_csv_for_all_symbols(file):
    symbols, caps = load_symbols_and_caps(file)
    for s in symbols:
        write_csv_for_one_symbol(s)
        
def write_csv_for_one_symbol(symbol):    
    newfile = base + symbol + '.csv' # name csv file to hold data of the stock symbol given
    data = pdr.get_data_yahoo(symbols = symbol, start = datetime(2015, 1, 1), end = datetime(2018, 11, 1))
    data.to_csv(newfile, encoding='utf-8')
