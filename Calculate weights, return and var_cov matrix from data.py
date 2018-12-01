import numpy 
#Functions get market capitilizaions from our chosen data
#and use these data to calculate weights, return and covariance
def compute_some_statistics(price_arrays):
    #Transfer a list of prices into a matrix
    price_up = numpy.mat(price_arrays)
    #Use our data to compute daily return
    price_row = numpy.size(price_up, 0)
    price_col = numpy.size(price_up, 1)
    data_return = numpy.zeros([price_row, price_col - 1])
    for i in range(price_row):
        for j in range(price_col - 1):
            p_start = price_up[i, j]
            p_end = price_up[i, j + 1]
            data_return[i, j] = (p_end - p_start)/ p_start      
    cal_return = numpy.array([])
    for i in range(price_row):
        mean_return = numpy.mean(data_return[i])
        cal_return = numpy.append(cal_return, mean_return)
    #Use our data to compute daily var_cov matrix  
    var_cov_matx = cov(data_return)
    #We assume that there are 250 tarding days in one year, and calculate annulized return
    #and annulized var_cov matrix
    cal_return = (1 + cal_return) ** 250 - 1
    var_cov_matx  = var_cov_matx * 250
    return cal_return, var_cov_matx

W = np.array(caps) / sum(caps)
Rp, Vp= compute_some_statistics(price_arrays)
#In practice, this 1.5% real risk-free rate is the rate that investors expect to earn after 
#inflation from a risk-free investment with a 10-year duration after inflation.
rf = 0.015
