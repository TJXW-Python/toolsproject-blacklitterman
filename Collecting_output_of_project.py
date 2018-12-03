#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  30 13:18:13 2018

@author: fiona.xue
"""

#Collect the optimal weight of 3 models
optimal_historical_data = optimal_portfolio_based_on_equilibrium_returns(Rp,Vp,rf)
optimal_implied_excess_return =optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)
optimal_adding_views = optimization_adding_views(Vp,view,view_link,Pi,rf)

## Display thewhole model using tables and graphs:
def OUTPUT_MODEL(optimal_historical_data,optimal_implied_excess_return,optimal_adding_views):
    graph_names(names,Rp,Vp,color='blue')
    graph_efficient_frontier(optimal_historical_data,label='Historical Data', color='blue')

    graph_names(names, Pi+rf, Vp, color='green')
    graph_efficient_frontier(optimal_implied_excess_return,label='Implied Equilibrium Excess Return', color='green')

    graph_names(names,optimal_adding_views['Pi']+rf, Vp, color='red')
    graph_efficient_frontier(optimal_adding_views,label='Adding views', color='red')

    xlabel('variance $\sigma$'), ylabel('mean $\mu$'), legend(), show()

    ##This part will output a table to tell the users their optimal weights 
    #on their selecting assets based on three given models:
    display(pandas.DataFrame({'Return': Rp, 'Weight (original_MV_opt)': weight_MV(Rp,Vp,rf),
                          'Weight (Reverse Optimization)': optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)['Weights'],
                          'Weight (reverse opt)': optimal_adding_views['Weights']}, index=names).T)
    display(pandas.DataFrame(Vp, columns=names, index=names))
