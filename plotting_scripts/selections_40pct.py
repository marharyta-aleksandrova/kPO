#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:19:04 2020

@author: mathcomp
"""

import matplotlib.pyplot as plt 
import numpy as np
import math
import tikzplotlib


my_area_to_select = 0.4

precision = 0.0000001

def samesign(a, b):
        return a * b > 0

def invert(funct, value, low, high):
    def bisect(func, low, high):
        'Find root of continuous function where f(low) and f(high) have opposite signs'
        assert not samesign(func(low), func(high))
        midpoint =0
        while abs(low-high) > precision:
            midpoint = (low + high) / 2.0
            if samesign(func(low), func(midpoint)):
                low = midpoint
            else:
                high = midpoint
        return midpoint
    def to_bissect(x):
        return funct(x)-value
    return bisect(to_bissect, low, high)


'product, i.e. k-pareto optimality'
def prod_area(k):
    if k == 0:
        return 0.0
    else:
        return k - k * math.log(k)
    
def sum_area(k):
    if k<1:
        return 0.5 * k*k
    else:
        return  0.5 * k*k -(k-1)*(k-1)


def min_k(area):
    return invert(lambda k: 2*k-k*k, area, 0, 1)

def max_k(area):
    return invert(lambda k: k*k, area, 0, 1)

def sum_k(area):
    return invert(lambda k: sum_area(k), area, 0, 1)

def prod_k(area):
    return invert(lambda k: prod_area(k), area, 0, 1)
    
my_min_k = min_k(my_area_to_select)
my_max_k = max_k(my_area_to_select)
my_sum_k = sum_k(my_area_to_select)
my_prod_k = prod_k(my_area_to_select)
#print("my_uniform_k: "+str(my_uniform_k))

x1_values =  np.linspace(0.0, 1, 1000)

def min_x2(x1, k):
    if x1 is None:
        return np.nan
    if x1 < k:
        return np.nan
    return k

def max_x2(x1, k):
    if x1 is None:
        return np.nan
    if x1 > k:
        return np.nan
    return k

def sum_x2(x1, k):
    if x1 is None:
        return np.nan
    if k-x1>1:
        return np.nan
    if x1 > k: 
        return np.nan
    return k-x1

def prod_x2(x1, k):
    if x1 is None:
        return np.nan
    if x1 < k:
        return np.nan
    return k/x1

min_x2_values = np.array(list(map(lambda x1: min_x2(x1, my_min_k), x1_values)))
max_x2_values = np.array(list(map(lambda x1: max_x2(x1, my_max_k), x1_values)))
sum_x2_values = np.array(list(map(lambda x1: sum_x2(x1, my_sum_k), x1_values)))
prod_x2_values = np.array(list(map(lambda x1: prod_x2(x1, my_prod_k), x1_values)))

# plotting the line 1 points
plt.plot(x1_values, min_x2_values, "k-",label = "min(x1,x2)") 
plt.plot(min_x2_values, x1_values, "k-", label='_nolegend_') 
plt.plot(x1_values, max_x2_values, "k:",label = "max(x1,x2)") 
plt.plot( max_x2_values, x1_values, "k:", label='_nolegend_') 
plt.plot(x1_values, sum_x2_values, "k-.",label = "x1+x2") 
plt.plot(x1_values, prod_x2_values, "k--",label = "x1*x2") 
plt.xlim(0, 1)
plt.ylim(0, 1) 
# naming the x axis 
plt.xlabel('x1') 
# naming the y axis 
plt.ylabel('x2') 
# giving a title to my graph 
#plt.title('impartiality for various utility functions!') 
  
# show a legend on the plot 
plt.legend() 
  
# function to show the plot 
plt.savefig('selections_40pct.png')
tikzplotlib.save("selections_40pct.tex", axis_height = '\\figH', axis_width = '\\figW')

plt.show() 
    

    
