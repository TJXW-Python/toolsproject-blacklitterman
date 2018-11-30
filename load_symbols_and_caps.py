from pandas import *


# Function loads stocks symbols and their market capitalizations, as of Nov 29, 2018
def load_symbols_and_caps(file):
    symbols_caps = pandas.read_csv(file, index_col = None) # symbols_caps is a pandas.dataframe
    symbols_caps.dropna(how = "all", inplace = True)
    symbols = list(symbols_caps['symbols'])
    caps = list(symbols_caps['caps'])
    return symbols, caps
