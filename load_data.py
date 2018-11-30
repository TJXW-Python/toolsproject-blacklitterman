from pandas import *


# Function loads historical stock prices of S&P companies mentioned in a CSV file and returns them together
# with their market capitalizations, as of Nov 29, 2018
def load_data(file):
    symbols, caps = load_symbols_and_caps(file)
    n = len(symbols)
    price_arrays = [] # array of close prices of each stock
    for s in symbols:
        data = pandas.read_csv('data/%s.csv' % s, index_col=None, parse_dates=['date']) # data is a pandas.dataframe
        prices = list(data['close'])
        price_arrays.append(prices) 
    return symbols, caps, price_arrays # price_arrays is an n*T list
