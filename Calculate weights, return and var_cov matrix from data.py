import numpy 

#Functions get market capitilizaions from our chosen data
#and use these data to calculate weights, return and covariance

def compute_some_statistics(price_arrays):
    price = numpy.array(price_arrays)
    
    price_row, price_col = price.shape
    data_return = numpy.zeros((price_row, price_col - 1))
    for r in range(price_row):
        for c in range(price_col - 1):
            p_start = price[r, c]
            p_end = price[r, c + 1]
            data_return[r, c] = (p_end - p_start)/ p_start
            
    cal_return = numpy.array([])
    for r in range(price_row):
        cal_return = append(cal_return, numpy.mean(data_return[r]))
    var_cov_matx = cov(data_return)
    cal_return = (1 + cal_return) ** 250 - 1
    var_cov_matx  = var_cov_matx * 250
    return cal_return, var_cov_matx

W = np.array(caps) / sum(caps)
Rp = compute_some_statistics(price_arrays)
Vp = compute_some_statistics(price_arrays)
rf = 0.015
