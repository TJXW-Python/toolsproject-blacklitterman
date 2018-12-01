from pandas import *

base = 'data/'
pool_file = base + 'SymbolsAndCaps.csv'

# Function extract market caps corresponding to the stock symbols entered by the user
# and also loads the historical stock prices and returns stock symbols, caps and historical prices
def load_data(assets_list):
    
    pool_symbols, pool_caps = load_symbols_and_caps(pool_file) # first load all symbols and caps in the pool
    
    symbols = assets_list
    caps = [] # extract market caps of the stocks chosen by the user
    for s in symbols:
        caps.append(pool_caps[pool_symbols.index(s)])

    price_arrays = [] # array of close prices of each stock chosen by the user
    for s in symbols:
        data = pandas.read_csv('data/%s.csv' % s, index_col=None, parse_dates=['date']) # data is a pandas.dataframe
        prices = list(data['close'])
        price_arrays.append(prices) 
    return symbols, caps, price_arrays # price_arrays is an n*T list
