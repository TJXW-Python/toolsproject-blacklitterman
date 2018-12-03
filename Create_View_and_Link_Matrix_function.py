#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 01:34:07 2018

@author: fiona.xue
"""

## This function is to produce the view matrix and view link matrix

from numpy import *

def matrix_view_and_link(symbols,view):
    #set view matrix
    view_=[]
    for i in view:
        for j in view[i]:
            view_.append(j)                
    view_matrix = [view_[i][2] for i in range(len(view_))]
    view_matrix =array([float(i) for i in view_matrix])
    
    #set an empty view link matrix 
    p_count = len(symbols)
    view_count = len(view_matrix)
    link_matrix= zeros([view_count,p_count]) 
    
    #refill the link matrix according to the view matrix
    i = 0
    symbols_index = dict()
    for asset in symbols:
        symbols_index[asset] = i
        i +=1
    for i in range(len(view_)):
        symbol_1=view_[i][0]
        symbol_2=view_[i][1]
        link_matrix[i,symbols_index[symbol_1]] = 1
        #recognize the absolute views and relative views
        if symbol_2:
            link_matrix[i,symbols_index[symbol_2]] = -1

    #use dictionary to return view and link matrix for further function
    View =dict()
    View['view_matrix']=view_matrix
    View['view_link']=link_matrix
          
    return View      
