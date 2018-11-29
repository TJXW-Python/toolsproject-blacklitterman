#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 11:16:23 2018

@author: fiona.xue
"""

def optimization_adding_views(Vp,view,view_link,pi):

    def pi_add_view(Vp,view,view_link,pi):
        pi_vol = dot(tau,Vp)    #the covariance matrix of equilibrium excess return
        view_vol= dot(dot(dot(tau,view_link),Vp),transpose(view_link))  # the covariance of adding views in k*k matrix
        pi_vol_inv = inv(pi_vol)  # inverse the covariance matrix of equilibrium excess return
        view_vol_inv = dot(dot(transpose(view_link),inv(view_vol)),view_link) # inverse the covariance of view in full matrix
        pi_view_weighted =dot(pi_vol_inv,pi)+dot(dot(transpose(view_link),inv(view_vol)),view) # the new equilibrium return weighted with variance 
        pi_new= dot(inv(view_vol_inv +pi_vol_inv), pi_view_weighted) #standardization
    
        return pi_new


    pi_new = pi_add_view(Vp,view,view_link,pi)
    Wp_new = weight_MV(pi_new+rf,Vp,rf)
    mean_new = sum(Wp_new * (pi_new+rf))
    var_new = dot(dot(Wp_new,Vp),Wp_new)
    mean_frontier, var_frontier = frontier_of_portfolio(pi_new+rf,Vp,rf)
    
    return pi_new,Wp_new,mean_new,var_new,mean_frontier, var_frontier
