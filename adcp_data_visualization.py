# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 16:33:56 2019

@author: User
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

##Insert path to your data
## Data provided by Ocean Networks Canada
data_path = 'C:/Users/User/Desktop/for_public_github/BarkleyCanyon_Axis_ADCP2MHz_20190308T045900Z_20190309T045850Z-NaN.csv'
head_dat = pd.read_csv(data_path, header=None)

## Remove the header from the data
end_head = (head_dat[head_dat[0]=='## END HEADER'].index[0]) + 1
end_pt = len(head_dat)                    
dat = head_dat.loc[end_head:end_pt, :]

## Rename the columns 
field_names = ['utc_time', 'compass_head', 'compass_flag', 'pitch', 'pitch_flag', 'pressure', 'pressure_flag', 'roll', 'roll_flag', 'sound_spd', 'sound_spd_flag', 'temp', 'temp_flag']                   
dat.columns = field_names  
order_dat = dat.reset_index(drop=True)

## Convert the utc time data into epoch time for easier plotting
for i in order_dat.index:
    temp_string = datetime.strptime(order_dat.utc_time[i], '%Y-%m-%dT%H:%M:%S.%fZ')
    temp_epoch = ((temp_string - datetime(1970,1,1)).total_seconds())
    order_dat.utc_time[i] = temp_epoch   

## Convert the data into numerical values
num_dat = order_dat.astype(np.number)

## Some summary statistics. I also verified that none of the flags were triggered
explore = num_dat.describe() 

## Remove the flag columns, as they are no longer needed
no_flag = num_dat.drop(['compass_flag', 'pitch_flag', 'pressure_flag', 'roll_flag', 'sound_spd_flag', 'temp_flag'], axis=1)

## Plot Time Vs. Temperature
plt.title('Temperature Vs. Time')
plt.plot(no_flag.utc_time, no_flag.temp)
plt.xlabel('Epoch time')  
plt.ylabel('Temperature(C)')
plt.savefig('C:/Users/User/Desktop/for_public_github/time_temp.png')
plt.show()

## Plot Time Vs. Sound speed
plt.title('Sound speed Vs. Time')
plt.plot(no_flag.utc_time, no_flag.sound_spd)
plt.xlabel('Epoch time')  
plt.ylabel('Sound speed(m/s)')
plt.savefig('C:/Users/User/Desktop/for_public_github/time_sound_spd.png')         
plt.show()

## Plot Time Vs. Pressure
plt.title('Pressure Vs. Time')
plt.plot(no_flag.utc_time, no_flag.pressure)
plt.xlabel('Epoch time')  
plt.ylabel('Pressure(decibar)')
plt.savefig('C:/Users/User/Desktop/for_public_github/time_pressure.png')
plt.show()

## A zoomed in plot of Time Vs. Pressure, to observe some of the finer structure
plt.title('Pressure Vs. Time')
plt.plot(no_flag.utc_time, no_flag.pressure)
plt.xlim(1552100000.785, 1552107530.785)
plt.xlabel('Epoch time')  
plt.ylabel('Pressure(decibar)')
plt.savefig('C:/Users/User/Desktop/for_public_github/cut_time_pressure.png')
plt.show()

## Plot a pearson correlation matrix for all the numerical data
corr_matrix = no_flag.corr()
plt.matshow(corr_matrix)
plt.title('Pearson Correlation matrix', pad=80)
plt.xticks(np.arange(7),('utc_time', 'compass_head', 'pitch', 'pressure', 'roll', 'sound_spd', 'temp'), rotation=70)
plt.yticks(np.arange(7),('utc_time', 'compass_head', 'pitch', 'pressure', 'roll', 'sound_spd', 'temp'))
plt.savefig('C:/Users/User/Desktop/for_public_github/corr.png')
plt.show()



