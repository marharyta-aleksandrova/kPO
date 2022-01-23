#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:19:04 2020

@author: mathcomp
"""

import matplotlib.pyplot as plt 
import numpy as np
import math

my_area_to_select = 0.1

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


def uniform_area(k):
    if k == 0:
        return 0.0
    else:
        return k - k * math.log(k)

def rarified_xi_area(k):
    if k == 0:
        return 0.0
    else:
        return k - k * math.log(k)

def rarified_x1x2_area(k):
    if k == 0:
        return 0.0
    else:
         return k - k * math.log(k)
   

def uniform_k(area):
    return invert(lambda k: uniform_area(k), area, 0, 1)
    
def rarified_xi_k(area):
    return invert(lambda k:  rarified_xi_area(k), area, 0, 1)

def rarified_x1x2_k(area):
    return invert(lambda k:  rarified_x1x2_area(k), area, 0, 1)
    
my_uniform_k = uniform_k(my_area_to_select)
print("my_uniform_k: "+str(my_uniform_k))
my_rarified_xi_k =  rarified_xi_k(my_area_to_select)
print("my_rarified_xi_k: "+str(my_rarified_xi_k))
my_rarified_x1x2_k =  rarified_x1x2_k(my_area_to_select)
print("my_rarified_x1x2_k"+str(my_rarified_x1x2_k))
x1_values =  np.linspace(0.0, 1, 1000)

def uniform_x2(x1, k):
    if x1 is None:
        return np.nan
    if x1 <= k:
        return np.nan
    return k/x1

def rarified_x2_x2(x1, k):
    if x1 <= k:
        return np.nan
    return math.sqrt(k/x1)

def rarified_x1x2_x2(x1, k):
    if x1 <= math.sqrt(k):
        return np.nan
    return math.sqrt(k)/x1

uniform_x2_values = np.array(list(map(lambda x1: uniform_x2(x1, my_uniform_k), x1_values)))
rarified_x2_x2_values = np.array(list(map(lambda x1: rarified_x2_x2(x1, my_rarified_xi_k), x1_values)))
rarified_x1x2_x2_values = np.array(list(map(lambda x1: rarified_x1x2_x2(x1, my_rarified_x1x2_k), x1_values)))
# plotting the line 1 points  
plt.plot(x1_values, uniform_x2_values, "k-",label = "uniform") 
plt.plot(x1_values, rarified_x2_x2_values, "k:",label = "rarified x2") 
plt.plot(x1_values, rarified_x1x2_x2_values, "k-.",label = "rarified x1x2") 
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
plt.savefig('rarification_dx2_2x2.png')
plt.show() 
    

    
