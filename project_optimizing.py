def frontier_of_portfolio(Rp,Vp,rf):
    exp_mean = []
    opt_var = []
    
    num_of_assets = len(Rp)
    
    min_ret = min(Rp)
    max_ret = max(Rp)
    group = 30 #Calculate 30 groups of optimal solution
    interval = (max_ret - min_ret)/(group - 1)
    ret_list = []
    for i in range(group):
        ret_list.append((min_ret + interval * i))
    def func_for_optimization(Wp,Rp,Vp,r):
        mean = dot(Wp,Rp)
        var = dot(dot(Wp,Vp),Wp)
        penalty = 10000 * abs(mean - r)
        #To guarantee that the mean of return of the portfolio should equal to r
        return var + penalty
    for r in ret_list:#The recursion should follows different target return
        Wp = ones(num_of_assets)/num_of_assets #The initial weight for optimization
        boundary = [] 
        for i in range(num_of_assets):
            boundary.append((0,1))
            #The boundary of each weight for a specific asset
        constraint_ = ({'type': 'eq', 'fun': lambda Wp: sum(Wp) - 1.0})
        #The constraints in optimizing that the sum of weights should equal to 1
        opt_result = scipy.optimize.minimize(
            func_for_optimization, Wp, (Rp, Vp, r), method = 'SLSQP',
            constraints = constraint_, bounds = boundary)
        
        if opt_result.success:
            exp_mean.append(r)
            opt_var.append(dot(dot(opt_result.x,Vp),opt_result.x))
        else:
            raise BaseException(opt_result.message)
    
    return array(exp_mean),array(opt_var)