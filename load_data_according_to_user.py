from pandas import *
from datetime import datetime
# terminal: $ pip install pandas-datareader
# or conda install -c anaconda pandas-datareader 
import pandas_datareader as pdr

base = 'data/'
pool_file = base + 'SymbolsAndCaps.csv'


assets_list = input('\n\nPlease type in the stock symbols you are interested in and separate them with a white space. For example, AMZN AAPL BRK-B\n\n') 
assets_list = select_assets(assets_list)

# Function loads stocks symbols and their market capitalizations, as of Nov 29, 2018
def load_symbols_and_caps(file):
    symbols_caps = pandas.read_csv(file, index_col = None) # symbols_caps is a pandas.dataframe
    symbols_caps.dropna(how = "all", inplace = True)
    symbols = list(symbols_caps['symbols'])
    caps = list(symbols_caps['caps'])
    return symbols, caps

def select_assets(*args):
    pool_symbols, _ = load_symbols_and_caps(pool_file)
    try:
        assets = ''.join(args).upper().split(' ')
    except:
        print('\n\nWarning: Illegal input!\n\n')
        return []
    if set(pool_symbols).union(set(assets)) != set(pool_symbols):
        print('\n\nWarning: Illegal input format or stock not in our pool! Please type again!\n\n')
        return []
    else:
        return assets


# Function extract market caps corresponding to the stock symbols entered by the user
# and also loads the historical stock prices and returns stock symbols, caps and historical prices
def load_data(assets_list):
    
    pool_symbols, pool_caps = load_symbols_and_caps(pool_file) # first load all symbols and caps in the pool
    
    symbols = list(set(assets_list)) # remove repeated symbols
    caps = [] # extract market caps of the stocks chosen by the user
    for s in symbols:
        caps.append(pool_caps[pool_symbols.index(s)])

    price_arrays = [] # array of close prices of each stock chosen by the user
    for s in symbols:
        data = pandas.read_csv('data/%s.csv' % s, index_col=None, parse_dates=True) # data is a pandas.dataframe
        prices = list(data['Close'])
        price_arrays.append(prices) 
    return symbols, caps, price_arrays # price_arrays is an n*T list
