import numpy as np

#Functions get market capitilizaions from our chosen data
#and use these data to calculate weights, return and covariance

def compute_some_statistics(price_arrays):
    price = np.array(price_arrays)
    
    price_row, price_col = price_arrays.shape
    data_return = np.zeros((price_row, price_col - 1))
    for r in range(price_row):
        for c in range(price_col - 1):
            p_start = price_arrays[r, c]
            p_end = price_arrays[r, c + 1]
            data_return[r, c] = (p_end - p_start)/ p_start
            
    cal_return = np.array([])
    for r in range(price_row):
        cal_return = append(expreturns, numpy.mean(returns[r]))
    var_cov_matx = cov(data_return)
    cal_return = (1 + expreturns) ** 250 - 1
    var_cov_matx  = var_cov_matx * 250
    return cal_return, var_cov_matx

W = np.array(caps) / sum(caps)
Rp = compute_some_statistics(price_arrays)
Vp = compute_some_statistics(price_arrays)
rf = 0.015
