#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  28 10:58:52 2018

@author: fiona.xue
"""
def optimal_final():
    display(pandas.DataFrame({'Return': Rp, 'Weight (original_MV_opt)': weight_MV(Rp,Vp,rf),
                          'Weight (Reverse Optimization)': optimal_portfolio_based_on_equilibrium_returns(Pi+rf,Vp,rf)['Weights'],
                          'Weight (reverse opt)': optimal_adding_views['Weights']}, index=names).T)
    display(pandas.DataFrame(Vp, columns=names, index=names))