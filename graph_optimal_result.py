#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 09:08:31 2018

@author: fiona.xue
"""


def graph_efficient_frontier(optimal,label=None, color='black'):
    text(optimal['Tangent_var'] ** .5, optimal['Tangent_mean'], '   tangent', verticalalignment='center', color=color)
    scatter(optimal['Tangent_var'] ** .5, optimal['Tangent_mean'], marker='o', color=color), grid(True)
    plot(optimal['Frontier_var'] ** .5, optimal['Frontier_mean'], label=label, color=color), grid(True)  # draw efficient frontie
def graph_names(names, Rp, Vp, color='black'):
    scatter([Vp[i, i] ** .5 for i in range(len(Rp))], Rp, marker='x', color=color), grid(True)  # draw assets
    for i in range(len(Rp)): 
        text(Vp[i, i] ** .5, Rp[i], '  %s' % names[i], verticalalignment='center', color=color) # draw labels


optimal_historical_data = optimal_portfolio_based_on_equilibrium_returns(Rp,Vp,rf)

optimal_implied_excess_return =optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)

optimal_adding_views = optimization_adding_views(Vp,view,view_link,Pi,rf)


graph_names(names,Rp,Vp,color='blue')
graph_efficient_frontier(optimal_historical_data,label='historical_data', color='blue')

graph_names(names, Pi+rf, Vp, color='green')

graph_efficient_frontier(optimal_implied_excess_return,label='Implied Equilibrium Excess Return', color='green')

graph_names(names,optimal_adding_views['Pi']+rf, Vp, color='red')

graph_efficient_frontier(optimal_adding_views,label='Adding views', color='red')
xlabel('variance $\sigma$'), ylabel('mean $\mu$'), legend(), show()