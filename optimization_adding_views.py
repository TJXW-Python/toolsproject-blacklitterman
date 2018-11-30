#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 11:16:23 2018

@author: fiona.xue
"""
# Calculate the optimization result after adding investers' views and relation matrix into the equilibrium excess return--"Pi"
def optimization_adding_views(Vp,view,view_link,pi,rf):
    scalar = 0.025                              #Scaling factor of blacklitterman moedl, set by Lee's paper, usually equals to 1 divided by observation numbers.
    def pi_add_view(Vp,view,view_link,pi):      #get the weighted equilibrium excess return based on primary pi and invester's view.
        pi_vol = dot(scalar,Vp)                    #weight is measured by uncertainty, this is the uncertainty matrix of equilibrium excess return: pi_vol (n*n matrix)
        view_vol= dot(dot(dot(scalar,view_link),Vp),transpose(view_link))  # the uncertainty of adding views: view_vol (k*k matrix)
        pi_vol_inv = inv(pi_vol)                # inverse the uncertainty matrix of equilibrium excess return
        view_vol_inv = dot(dot(transpose(view_link),inv(view_vol)),view_link) # inverse the uncertainty of view (n*n matrix)
        pi_view_weighted =dot(pi_vol_inv,pi)+dot(dot(transpose(view_link),inv(view_vol)),view) # the new equilibrium return weighted by the inverse of uncertainty
        pi_new= dot(inv(view_vol_inv +pi_vol_inv), pi_view_weighted)  #standardization
    
        return pi_new                           #return the weighted pi

    # get the optimal allocation weights and efficent frontier based on new equilibrium excess return
    pi_new = pi_add_view(Vp,view,view_link,pi)   
    Wp_new = weight_MV(pi_new+rf,Vp,rf)
    mean_new = sum(Wp_new * (pi_new+rf))
    var_new = dot(dot(Wp_new,Vp),Wp_new)
    mean_frontier, var_frontier = frontier_of_portfolio(pi_new+rf,Vp,rf)
    
    return Wp_new,mean_new,var_new,mean_frontier, var_frontier # return all the result in an array
