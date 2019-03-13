# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 13:58:07 2019

@author: User
"""

#%%

import datetime
import numpy as np
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

## Use requests to get data from the Trackie web page            
URL = 'https://www.trackie.com/USports/TNF/Rankings/wommens-3000-meter/11/'

r = requests.get(URL)
 
## Get HTML table
soup = bs(r.content,'html5lib')    
table = soup.find("table", attrs={"style":"width: 670px;"}) 

## Extract data from HTML table
datasets = []
for row in table.find_all("tr")[1:]:
    dataset = (td.get_text() for td in row.find_all("td"))
    datasets.append(dataset)

## Place data from HTML table into a dict with athlete's name as the key
data_dict = {}
count = 0
for dataset in datasets:
    temp_list = []
    for field in dataset:
        temp_list.append(field)
        
    data_dict[temp_list[1]] = temp_list
    count = count + 1
    


def get_sec(time_str):
    ''' Gets the minutes, seconds, and milliseconds from a string and
    returns these as integers'''
    m,s = time_str.split(':')
    int_s, ms = s.split('.')
    return int(m) , int(int_s), int(ms)

## Converts the string entries in data_dict to usable datetime vlues
times = []    
for key in data_dict.keys():
    inmin = get_sec(data_dict[key][3][0:7])[0]
    ins = get_sec(data_dict[key][3][0:7])[1]
    inms = get_sec(data_dict[key][3][0:7])[2]
    data_dict[key][3] = datetime.time(0, inmin, ins, inms)
    times.append(data_dict[key][3])

## Make a plot of times vs. rank. Interesting shape.    
sort_times = sorted(times)
plt.plot(sort_times, 'o', markersize=3)
plt.xlabel('Usports Ranking')
plt.grid()    
plt.savefig('../images/time_vs_rank.png')
plt.show()


##This is dubious, getting unreasonable fastest time and improper labels for higher times
#total_secs = []

#for time in sort_times:
#    total_secs.append(time.minute*60 + time.second)
 
#string_time = []
#for secs in total_secs:
#    minutes = secs//60
#    seconds = secs%60
#    string_time.append(str(minutes)+':'+str(secs))
    
#length = len(total_secs)
   
#sec_bins = []
#str_bins = [] 
#for i in range(0, length, length//10):
#    sec_bins.append(total_secs[i])
#    str_bins.append(string_time[i][0:4]+'.'+string_time[i][4])
#    
#plt.hist(total_secs)
#plt.xticks(sec_bins, str_bins, rotation=45)
#plt.show()

