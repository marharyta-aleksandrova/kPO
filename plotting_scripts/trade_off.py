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

my_area_to_select = 0.25
# a here is the inverse of the a in the paper
my_tradeoff_a =[0.5, 2, 10]
my_linestyle=["k:","k-.","k--"]
my_linelabel=["a=2","a=0.5","a=0.1"]
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
    
def tradeoff_y(x, a, k):
    triangle=0.5*a*(1-x)*(1-x)
    rectangle = x*a*(1-x)
    if rectangle+triangle>=k:
        return min(max(0,-a*x+math.sqrt(a*a*x*x+2*a*k)),1)
    else:
        return min(max(0,k+triangle),1)
                       
def tradeoff_area(a,k):
    integral, _ = integrate.quad(lambda x: tradeoff_y(x, a, k), 0, 1)
    return integral

def tradeoff_k(area, a):
    return invert(lambda k: tradeoff_area(a,k), area, 0, 1)
         
    
my_tradeoff_k = []
for a in my_tradeoff_a:
    my_tradeoff_k.append(tradeoff_k(my_area_to_select, a))
    
x1_values =  np.linspace(0.0, 1, 1000)

def tradeoff_x2_values(x1, a, k):
    float_result = tradeoff_y(x1, a, k)
    if float_result <= 0 or float_result>=1:
        return np.nan
    else:
        return float_result
    
my_tradeoff_x2_values=[]
for i in range(len(my_tradeoff_a)):
    my_tradeoff_x2_values.append(np.array(list(map(lambda x1: tradeoff_x2_values(x1, my_tradeoff_a[i], my_tradeoff_k[i]), x1_values))))

# plotting the line 1 points  
for i in range(len(my_tradeoff_a)):
    plt.plot(x1_values, my_tradeoff_x2_values[i], my_linestyle[i],label = my_linelabel[i]) 
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
#plt.savefig('tradeoff.png')
plt.show() 
    

    
