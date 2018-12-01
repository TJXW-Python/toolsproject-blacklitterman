import numpy 
#Functions get market capitilizaions from our chosen data
#and use these data to calculate weights, return and covariance

def compute_some_statistics(price_arrays):
    price = numpy.array(price_arrays)
    
    price_row, price_col = price.shape
    data_return = numpy.zeros([price_row, price_col - 1])
    for i in range(price_row):
        for j in range(price_col - 1):
            p_start = price[i, j]
            p_end = price[i, j + 1]
            data_return[i, j] = (p_end - p_start)/ p_start
            
    cal_return = numpy.array([])
    for i in range(price_row):
        cal_return = append(cal_return, numpy.mean(data_return[i]))
    var_cov_matx = cov(data_return)
    #We assume that there are 250 tarding days in one year, and calculate annulized return
    #and annulized var_cov matrix
    cal_return = (1 + cal_return) ** 250 - 1
    var_cov_matx  = var_cov_matx * 250
    return cal_return, var_cov_matx

W = np.array(caps) / sum(caps)
Rp, Vp= compute_some_statistics(price_arrays)
rf = 0.015
