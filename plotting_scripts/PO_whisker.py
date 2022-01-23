#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:19:04 2020

@author: mathcomp
"""

import matplotlib.pyplot as plt 
import numpy as np
import math
from scipy import integrate


my_area_to_select = 0.1 #selecting 20 percent of the shaded area
# a here is the inverse of the a in the paper
whisker_linestyle="k-"
whisker_linelabel="Po sort"
nsgaii_linestyle="k-."
limit_linestyle="k-"
nsgaii_linelabel="front sort"
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
    
def whisker_y(x, k):
    def f_A(x, k):
        return 0.5-x
    def f_B(x, k):
        return -x+math.sqrt(2*k)+0.5
    def f_C(x, k):
        return -0.5*x+(k/x)+0.5
    def f_D(x, k):
        return math.sqrt((x-0.5)*(x-0.5)+2*k)+0.5-x
    if k ==0:
        return f_A(x, k)
    else:
        if x > 0.5: 
            return f_D(x, k)
        elif x > math.sqrt(2*k): 
            return f_B(x, k)
        elif x>k:
            return f_C(x, k)
        else:
            return 1
        
                       
def whisker_area(k):
    integral, _ = integrate.quad(lambda x: whisker_y(x, k), 0, 1)
    return integral - 0.125

def whisker_k(area):
    return invert(lambda k: whisker_area(k), area, 0.0001, 0.125)
         
    
my_whisker_k = whisker_k(my_area_to_select)
    
x1_values =  np.linspace(0.0, 1, 2500)

def whisker_x2_values(x1, k):
    float_result = whisker_y(x1, k)
    if float_result <= 0 or float_result>=1:
        return np.nan
    else:
        return float_result

def flip(np_array):
     return np_array
#    return 1-np_array

def reflip(np_array):
     return 1-np_array
#    return np_array
     
def l_bound(x):
    if x <0.5:
        return 0.75-0.5*x
    elif x<0.75:
        return 0.5-2*(x-0.5)
    else:
        return 0
    
def u_bound(x):
    if x<0.5:
        return 1
    else:
        return 1-(x-0.5)
    
my_whisker_x2_values= np.array(list(map(lambda x1: whisker_x2_values(x1, my_whisker_k), x1_values)))
my_nsgaii_x2_values= np.array(list(map(lambda x1: math.sqrt(2*my_area_to_select+0.25)-x1, x1_values)))
u_bound_x2_values= np.array(list(map(lambda x1: u_bound(x1), x1_values)))
l_bound_x2_values= np.array(list(map(lambda x1: l_bound(x1), x1_values)))

plt.plot( flip(x1_values), flip(my_whisker_x2_values),whisker_linestyle,label =whisker_linelabel) 
plt.plot(flip(x1_values), flip(my_nsgaii_x2_values), nsgaii_linestyle,label =nsgaii_linelabel) 
#plt.plot(x1_values, u_bound_x2_values, limit_linestyle) 
#plt.plot(x1_values, l_bound_x2_values, limit_linestyle) 
plt.fill_between(reflip(x1_values), reflip(l_bound_x2_values), reflip(u_bound_x2_values),  hatch="....", facecolor='lightgrey',edgecolor='dimgray')
plt.plot()
plt.axes().set_aspect('equal', adjustable='box')

plt.xlim(0, 1)
plt.ylim(0, 1) 
# naming the x axis 
plt.xlabel('x1') 
# naming the y axis 
plt.ylabel('x2') 
# set ticks and 
plt.xticks([])
plt.yticks([])
# giving a title to my graph 
#plt.title('impartiality for various utility functions!') 
  
# show a legend on the plot 
plt.legend() 
  
# function to show the plot 
plt.savefig('whisker.png')
plt.show() 
    

    
