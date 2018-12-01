#He and Litterman (1999) propose considering τ as the ratio of the sampling variance 
#to the distribution variance, and thus it is 1/t.

#τ is a measure of the investor’s confidence in the prior
#estimates, and as such it is largely a subjective factor
#τ =   A scalar number indicating the uncertainty of the CAPM distribution (0.025-0.05)
# τ too high makes a very weak statement for our prior estimate of the mean.
def optimization_adding_views(Vp,view,view_link,Pi,rf):

    def pi_add_view(Vp,view,view_link,Pi):  
        scalar = numpy.linspace(0.025, 0.05, 6)      # scaling factor for blacklitterman model is set according to Lee's paper
        ##weight is measured by uncertainty, this is the uncertainty matrix of equilibrium excess return: pi_vol (n*n matrix)
        scalar_list = list(scalar)
        pi_new_list = []
        for i in scalar_list:
            pi_vol = dot(i,Vp)                    
            view_vol= dot(dot(dot(i,view_link),Vp),transpose(view_link))  
            pi_vol_inv = inv(pi_vol)                
            view_vol_inv = dot(dot(transpose(view_link),inv(view_vol)),view_link) 
            pi_view_weighted =dot(pi_vol_inv,Pi)+dot(dot(transpose(view_link),inv(view_vol)),view) 
            pi_new= dot(inv(view_vol_inv +pi_vol_inv), pi_view_weighted) 
            pi_new_list = pi_new_list.append(pi_new)
        ##the new equilibrium return weighted by the inverse of uncertainty and standardization
    
        return pi_new_list                         

    # get the optimal allocation weights and efficent frontier based on new equilibrium excess return
    len_list = len(pi_new_list)
    pi_new_list = pi_add_view(Vp,view,view_link,Pi)  
    Wp_new_list =[weight_MV(i + rf,Vp,rf) for i in pi_new_list] 
    mean_new_list = [sum(Wp_new_list[i] * (pi_new_list[i] + rf)) for i in range(len_list)]
    var_new_list = [dot(dot(Wp_new_list[i],Vp),Wp_new_list[i]) for i in range(len_list)]

    mean_frontier_list = []
    var_frontier_list = []   
    for i in range(len_list):
        mean_frontier, var_frontier = frontier_of_portfolio(pi_new_list[i] + rf, Vp, rf)
        mean_frontier_list = mean_frontier_list.append(mean_frontier)
        var_frontier_list = var_frontier_list.append(var_frontier)
    
    result_adding_views_list = []
    for i in range(len_list):
        result_adding_views = dict()
        result_adding_views['Pi'] = pi_new_list[i]
        result_adding_views['Weights'] = Wp_new_list[i]
        result_adding_views['Tangent_mean'] = mean_new_list[i]
        result_adding_views['Tangent_var'] = var_new_list[i]
        result_adding_views['Frontier_mean'] = mean_frontier_list[i]
        result_adding_views['Frontier_var'] = var_frontier_list[i]
        
        result_adding_views_list = result_adding_views_list.append(result_adding_views)
    return result_adding_views_list
  
