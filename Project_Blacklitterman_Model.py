#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:46:54 2018

@author: fiona.xue
"""
%pylab
import scipy.optimize
from numpy import *
from pandas import *
import re



##At the beginning of the project######################################################################
#We need to ask users to provide the assets they would like to invest##################################
print('Welcome to use the Blacklitterman Model project.')
print('Based on the performance, we provided 20 assets that are worthy investing.')
print('The symbols of these 20 assets are as follows:')
print('1 GE; 2 CVX; ...')
print('Please select assets that you want to invest: ')
print('(Enter the number of the assets, e.g. if you want to invest GE, type in 1; CVX for 2;...)')
illegal_asset = 100
judgement = 0
print('(Please use list to type in, e.g. [1,4,6,7,9])')
while illegal_asset > 0 or judgement < 1:
    number_of_assets = input('hhaha')
    pattern1 = r'[0-9.]+'
    type_in_assets = re.findall(pattern1,number_of_assets)
    illegal_asset = 0
    select_assets = []
    for i in type_in_assets:
        a = int(float(i))
        if a < 0 or a > 20 or a != float(i):
            illegal_asset += 1
            print('Please type in integer numbers between 1-20!')
        exist = 0
        for j in select_assets:
            if j == a:
                exist += 1
        if exist >= 1:
            continue
        else:
            select_assets.append(a)
    if illegal_asset == 0:
        print(f'Your choices are assets: {select_assets}')
        print('Please verify your choice: 1 for Yes, 0 for No.')
        judge = input('judge = ')
        if int(float(judge)) == 1:
            judgement == 1
            break
        else:
            judgement == 0
            print('Please choose again:')
print(f'Your choices are assets: {select_assets}')

################################################################################################

##The function to calculate the valid frontier of portfolio constructed with given assets##
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
    # For given level of return r, find weights which minimizes portfolio variance.  
    def func_for_optimization(Wp,Rp,Vp,r):
        mean = dot(Wp,Rp)
        var = dot(dot(Wp,Vp),Wp)
        penalty = 100 * abs(mean - r)
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
###############################################################################################

##This function is used to calculate tangent point based on optimal portfolio and risk-free rate
def weight_MV(Rp,Vp,rf):
    def weight_initial(Rp):                 # initial weight of the optimization procedure
        port_count = len(Rp)
        Wp=[]
        for i in range(port_count):
            Wp.append(1/port_count)         # set all of these assets with equal weights in the portfolio
        return Wp
    def MV_object_function(Wp,Rp,Vp,rf):    # return the objective function of MV_optimization $$$$$$$$change 
        p_mean = sum(Rp*Wp)                 #calculate the mean return of the portfolio
        p_var = dot(dot(Wp,Vp),Wp)          #calculate the variance of the portfolio
        p_sharp_ratio= (p_mean - rf) / sqrt(p_var)
        object_func =  1 / p_sharp_ratio
        return object_func
    def MV_optimal(Rp,Vp,rf):
        Wp = weight_initial(Rp)              # input the initial weight
        bound = []                           # add each bound of every assets weight in the spread from [0,1]
        for i in range(len(Rp)):
            bound.append((0.,1.))                 
        constraint = ({'type': 'eq',         # give the constraints of optimization problem, the sum of weight equals to 1.0
                          'fun': lambda Wp: sum(Wp) - 1.}) 
        weight_optimal =scipy.optimize.minimize(MV_object_function, 
                                                Wp,(Rp,Vp,rf),method='SLSQP',constraints=constraint, bounds=bound)
                                             #calculate the optimal weight of each assests in the portfolio in MV model
        if weight_optimal.success:
            return weight_optimal.x
        else:
            raise BaseException(weight_optimal.message)
    return MV_optimal(Rp,Vp,rf)
#####################################################################################################################

##This part is used to optimize the portfolio based on equilibrium excess return##
def optimal_portfolio_based_on_equilibrium_returns(Rp,Vp,rf):
    Wp = weight_MV(Rp,Vp,rf)
    opt_mean = dot(Wp,Rp)
    opt_var = dot(dot(Wp,Vp),Wp)
    frontier_mean,frontier_var = frontier_of_portfolio(Rp,Vp,rf)
    result_implied_return = dict()
    result_implied_return['Weights']=Wp
    result_implied_return['Tangent_mean']=opt_mean
    result_implied_return['Tangent_var']=opt_var
    result_implied_return['Frontier_mean']=frontier_mean
    result_implied_return['Frontier_var']=frontier_var
    return result_implied_return

##W is the market capitalization weights
def equilibrium_excess_return(W,Rp,Vp):
    mean = dot(W,Rp)
    var = dot(dot(W,Vp),W)
    lamuda = (mean - rf)/var
    return dot(dot(lamuda,Vp),W)

Pi = equilibrium_excess_return(W,Rp,Vp)##Using market capitalization weight W

result_eq = optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)

###################################################################################

## This part is used to optimize the portfolio based on equilibrium excess return 
## after adding investers' views and relation matrix into the equilibrium excess return--"Pi"
def optimization_adding_views(Vp,view,view_link,Pi,rf):

    def pi_add_view(Vp,view,view_link,Pi):  
        scalar = 0.025       # scaling factor for blacklitterman model is set according to Lee's paper
        ##weight is measured by uncertainty, this is the uncertainty matrix of equilibrium excess return: pi_vol (n*n matrix)
        pi_vol = dot(scalar,Vp)                    
        view_vol= dot(dot(dot(scalar,view_link),Vp),transpose(view_link))  
        pi_vol_inv = inv(pi_vol)                
        view_vol_inv = dot(dot(transpose(view_link),inv(view_vol)),view_link) 
        pi_view_weighted =dot(pi_vol_inv,Pi)+dot(dot(transpose(view_link),inv(view_vol)),view) 
        pi_new= dot(inv(view_vol_inv +pi_vol_inv), pi_view_weighted)  
        ##the new equilibrium return weighted by the inverse of uncertainty and standardization
    
        return pi_new                          

    # get the optimal allocation weights and efficent frontier based on new equilibrium excess return
    pi_new = pi_add_view(Vp,view,view_link,Pi)   
    Wp_new = weight_MV(pi_new+rf,Vp,rf)
    mean_new = sum(Wp_new * (pi_new+rf))
    var_new = dot(dot(Wp_new,Vp),Wp_new)
    mean_frontier, var_frontier = frontier_of_portfolio(pi_new+rf,Vp,rf)
    
    result_adding_views= dict()
    result_adding_views['Pi']=pi_new
    result_adding_views['Weights']=Wp_new
    result_adding_views['Tangent_mean']=mean_new
    result_adding_views['Tangent_var']=var_new
    result_adding_views['Frontier_mean']=mean_frontier
    result_adding_views['Frontier_var']=var_frontier
    return result_adding_views
  
######################################################################################################

##This function is used to draw efficient frontier of given assets
def graph_efficient_frontier(optimal,label=None, color='black'):
    text(optimal['Tangent_var'] ** .5, optimal['Tangent_mean'], '   tangent', verticalalignment='center', color=color)
    scatter(optimal['Tangent_var'] ** .5, optimal['Tangent_mean'], marker='o', color=color), grid(True)
    plot(optimal['Frontier_var'] ** .5, optimal['Frontier_mean'], label=label, color=color), grid(True) 
    
##This function is used to add nodes pof assets and mark labels to each nodes in the graph
def graph_names(names, Rp, Vp, color='black'):
    scatter([Vp[i, i] ** .5 for i in range(len(Rp))], Rp, marker='x', color=color), grid(True)  
    for i in range(len(Rp)): 
        text(Vp[i, i] ** .5, Rp[i], '  %s' % names[i], verticalalignment='center', color=color) 

#Collect the optimal weight of 3 models
optimal_historical_data = optimal_portfolio_based_on_equilibrium_returns(Rp,Vp,rf)
optimal_implied_excess_return =optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)
optimal_adding_views = optimization_adding_views(Vp,view,view_link,Pi,rf)


graph_names(names,Rp,Vp,color='blue')
graph_efficient_frontier(optimal_historical_data,label='Historical Data', color='blue')

graph_names(names, Pi+rf, Vp, color='green')
graph_efficient_frontier(optimal_implied_excess_return,label='Implied Equilibrium Excess Return', color='green')

graph_names(names,optimal_adding_views['Pi']+rf, Vp, color='red')
graph_efficient_frontier(optimal_adding_views,label='Adding views', color='red')

xlabel('variance $\sigma$'), ylabel('mean $\mu$'), legend(), show()
