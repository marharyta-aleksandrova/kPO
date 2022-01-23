
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:19:04 2020

@author: mathcomp
"""

import matplotlib.pyplot as plt 
import matplotlib
import numpy as np
import math
import tikzplotlib

#my_area_to_select = 0.4

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


def prod_area(k):
    if k == 0:
        return 0.0
    else:
        return k - k * math.log(k)

def prod_choice(k):
	return (k-k*math.log(k))*(k-k*math.log(k))-k*k*(0.5-math.log(k))

def prod_diversity(area): 
	if area==0: 
		return 1
	else:
		k = invert(lambda k: prod_area(k), area, 0, 1) 
		return prod_choice(k)/(area*area)

def sum_area(k):
	if k<1:
		return 0.5*k*k
	else:
		return 0.5*k*k - (k-1)*(k-1)


def sum_po_integral(k):
	if k <= 1:
		return (1/24)*k*k*k*k
	elif k>1:
		return (1/4)*(k-1)*(k-1) + 1/8 -k/3+(k*k)/4 -(1/8)*(k-1)**4 +(1/3)*k*(k-1)**3 - (1/4)*k*k*(k-1)*(k-1)

def sum_diversity(area): 
	if area==0: 
		return 2/3
	else:
		k = invert(lambda k: sum_area(k), area, 0, 2) 
		return (area*area-2*sum_po_integral(k))/(area*area)


def max_diversity(area):   
		return 0.5


def min_area(k):
		return 2*k-k*k


def min_po_integral(k):
		return k*(k/4)*(2-k*k)


def min_diversity(area):    
	if area==0: 
		return 3/4
	else:
		k = invert(lambda k: min_area(k), area, 0, 1) 
		return (area*area-2*min_po_integral(k))/(area*area)

areas =  np.linspace(0.0, 1, 100)  
		

min_diversities = np.array(list(map(lambda area: min_diversity(area), areas)))
max_diversities = np.array(list(map(lambda area: max_diversity(area), areas)))
sum_diversities = np.array(list(map(lambda area: sum_diversity(area), areas)))
prod_diversities = np.array(list(map(lambda area: prod_diversity(area), areas)))

# plotting the line 1 points
# default: matplotlib.rcParams['figure.figsize'] = [8.0, 6.0]
matplotlib.rcParams['figure.figsize'] = [2.5, 2.0]
plt.plot(areas, min_diversities, "k-",label = "min(x1,x2)") 
plt.plot(areas, max_diversities, "k:",label = "max(x1,x2)") 
plt.plot(areas, sum_diversities, "k-.",label = "x1+x2") 
plt.plot(areas, prod_diversities, "k--",label = "x1*x2") 

plt.xlim(0, 1)
plt.ylim(0, 1) 
# naming the x axis 
plt.xlabel('percentage selected') 
# naming the y axis 
plt.ylabel('diversity') 
# giving a title to my graph 
#plt.title('impartiality for various utility functions!') 
  
# show a legend on the plot 
plt.legend(loc='lower right') 
  
# function to show the plot 
plt.savefig('diversity_vs_area.png')
tikzplotlib.save("diversity_vs_area.tex", axis_height = '\\figH', axis_width = '\\figW')

plt.show() 
    
