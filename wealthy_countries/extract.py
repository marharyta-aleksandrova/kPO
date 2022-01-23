#!/usr/bin/python3

import pprint
import csv
import math
import numbers

#data files, contain values for a given year (2013)
population_file = 'Population, total (millions).csv'
expected_schooling_file='Expected years of schooling (years).csv'
mean_schooling_file='Mean years of schooling (years).csv'
life_expectancy_file='Life expectancy at birth (years).csv'
gni_file='Gross national income (GNI) per capita (2011 PPP$).csv'
hdi_file='Human Development Index (HDI).csv'


label_column_name ='Country'
value_column_name = '2015'
n_variables = 13+1
# position of the variable in the storage list
country_i = 0
unit_i=1
population_i = 2
expected_schooling_i = 3
mean_schooling_i =4
life_expectancy_i=5
gni_i=6
hdi_i=7
purehdi_i=8
po_i=9
weight_tk_i=10
chob_i=11
div_i =12
is_poor_i=13
colnames =['country', 'unit', 'population', 'expected_schooling', 'mean_schooling', 'life_expectancy', 'gni', 'hdi', 'purehdi', 'po', 'weight_tk', 'chob','div','is_poor']
weight_i = unit_i
#store education at position 1 of value
countries_dict={}
 
def add_value(country,  i,  value):
    if not country in countries_dict:
        countries_dict[country]=[None]*n_variables
        countries_dict[country][unit_i]=1
        countries_dict[country][country_i]=country
    countries_dict[country][i]=value

def read_values(file_name,  label_column_name,  value_column_name,  value_i):
    with open(file_name, mode='r',   encoding="iso-8859-1") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if label_column_name in row and value_column_name in row:
                    csv_value = row[value_column_name]
                    if isinstance(csv_value,str):
                        try:
                            csv_value = csv_value.split(None, 1)[0]
                        except IndexError:
                            print("impossible to extract number ",  file_name, ",ignored line: ",  reader.line_num,  'csv_value: ',  csv_value)
                    if csv_value is None:
                       csv_value = row[value_column_name]
                    if csv_value is None:
                       csv_value = 'empty'
                    add_value(row[label_column_name],  value_i,  float(csv_value))
                else:
                    print(file_name,', ignored line:', reader.line_num , end='', flush=True)
                    for k,  v in row:
                        print(str(v), end='', flush=True)
                    print("\n", end='', flush=True)
            except ValueError:
                print(file_name, ",ignored line: ",  reader.line_num ,  ": not a float! ", row[label_column_name],' ',  csv_value)
                
    
def purehdi(expected_schooling,  mean_schooling,  life_expectancy):    
    return math.sqrt(  (((expected_schooling/max_expected_schooling)+(mean_schooling/max_mean_schooling))/2.0) * ((life_expectancy-20)/(85-20.0)) )
    
def other_strictly_better(element,  other):
    if other[gni_i] ==element[gni_i] and other[purehdi_i]==element[purehdi_i]:
        return False
    else:
        return  other[gni_i] >=element[gni_i] and other[purehdi_i]>=element[purehdi_i]
    
def is_not_number(row,  colname,  index):
    if isinstance(row[index], numbers.Number):
        return False
    else:
        print('deleted, missing ',  colname,  ', value: ', row[index],  ',  country: ',  row[country_i] )
        return True

def max_value(sample,  i):
    result = 0
    for element in sample:
        result = max(element[i], result)
    return result

def no_missing_values(row):
    if is_not_number(row, 'weight', weight_i):
        return False
    if  is_not_number(row, 'expected_schooling', expected_schooling_i):
        return False
    if is_not_number(row,  'mean_schooling',  mean_schooling_i):
        return False
    if is_not_number(row,  'life_expectancy',  life_expectancy_i):
        return False
    if is_not_number(row,  'gni',  gni_i):
        return False
    return True

#read data
read_values(population_file,  label_column_name,  value_column_name,  population_i)
read_values(expected_schooling_file,   label_column_name,  value_column_name,  expected_schooling_i)
read_values(mean_schooling_file,   label_column_name,  value_column_name,  mean_schooling_i)
read_values(life_expectancy_file,   label_column_name,  value_column_name,  life_expectancy_i)
read_values(gni_file,   label_column_name,  value_column_name,  gni_i)
read_values(hdi_file,   label_column_name,  value_column_name,  hdi_i)
#delete from sample if no weight, expected_schooling, mean_schooling, life_expectancy, gni
sample = list(filter(lambda x: no_missing_values(x),  countries_dict.values()))
#compute pure_hdi
max_mean_schooling=max_value(sample,  mean_schooling_i)
max_expected_schooling=max_value(sample,  expected_schooling_i)
for element  in sample:
    element[purehdi_i]=purehdi(element[expected_schooling_i],  element[mean_schooling_i],  element[life_expectancy_i])
#compute pareto optimality
for element in sample:
    po=0
    for other in sample:
        if other_strictly_better(element,  other):
            po+=other[weight_i]
    element[po_i]=po
#compute diversities using the following formula
#cho(t_k) = weight(t_k)^2 -2 chob(t_k), where chob(t_k)=weight_teqk *po
sample = sorted(sample,  key= lambda x:x[po_i])
cum_weight = 0
chob=0
for element in sample:
    chob+=element[weight_i]*element[po_i]
    cum_weight+=element[weight_i]
    element[div_i]=1 -2*chob/(cum_weight*cum_weight)
    if  element[div_i]<0.5:
        element[is_poor_i]=True
    else:
        element[is_poor_i]=False
        
#treat the cases where several elements have the same po
last_i =  len(sample)-1
previous_i =0
i =0
while i <=last_i:
    if sample[i][po_i]!=sample[i][previous_i] or i==last_i:
        for j in range(previous_i,  i):
            sample[j][div_i] = sample[previous_i][div_i]
            previous_i =j+1
    i+=1
    
#output results
sample.insert(0,  colnames)
with open("output.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(sample)
