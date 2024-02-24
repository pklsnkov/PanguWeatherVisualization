'''
Основная статья
https://www.earthinversion.com/utilities/reading-NetCDF4-data-in-python/
'''

import netCDF4
import numpy as np
import os
import shutil

# import sys
# day_num = sys.argv[1]

def nc2npy(day_num):
     surface_dataset = netCDF4.Dataset('netCDF4_input_data\\surf.nc')
     upper_dataset = netCDF4.Dataset('netCDF4_input_data\\upper.nc')

     surface_variables = surface_dataset.variables.keys()
     upper_variables = upper_dataset.variables.keys()

     # if not os.path.isdir('test_input_data'):
     #      os.mkdir('test_input_data')
     # else:
     #      shutil.rmtree('test_input_data')
     #      os.mkdir('test_input_data')

     surface_data_dict = {}
     upper_data_dict = {}

     surface_data_list = []
     upper_data_list = []
     surface_data_list_few_day = []
     upper_data_list_few_day = []


     dim_list_surf = surface_dataset.dimensions.keys()
     dim_list_upper = upper_dataset.dimensions.keys()

     dict_reserve = {
          'msl': [],
          'u10': [],
          'v10': [],
          't2m': [],
     }
     order_list = ['msl', 'u10', 'v10', 't2m']
     # day_num = 6
     first_flag = True
     surface_data_list = [[], [], [], []]
     surface_data_list_few_day = [[], [], [], []]
     # len_dim = 0
     for variable_name in surface_variables:
          if variable_name in dim_list_surf:
               # len_dim+=1
               continue
          start_data = surface_dataset.variables[variable_name][0, :, :]
          few_day_data = surface_dataset.variables[variable_name][day_num*24/6, :, :]
          
          index = order_list.index(variable_name)
          surface_data_list[index] = start_data
          surface_data_list_few_day[index] = few_day_data

     order_list = ['z', 'q', 't', 'u', 'v']
     first_flag = True
     upper_data_list = [[], [], [], [], []]
     upper_data_list_few_day = [[], [], [], [], []]

     pressure_upper_data = upper_dataset.variables['level'][:]
     for variable_name in upper_variables:
          if variable_name in dim_list_upper:
               continue
          start_data = upper_dataset.variables[variable_name][0, :, :, :] # .filled()
          start_data_flip = np.flip(start_data, axis=0)
          few_day_data = upper_dataset.variables[variable_name][day_num*24/6, :, :, :]
          few_day_data_flip = np.flip(few_day_data, axis=0)
          
          index = order_list.index(variable_name)
          upper_data_list[index] = start_data_flip
          upper_data_list_few_day[index] = few_day_data_flip

     surface_dataset.close()
     upper_dataset.close()

     print('Начало сохранения')

     surf_arr = np.array(surface_data_list)
     upper_arr = np.array(upper_data_list)
     np.save(os.path.join('test_input_data','input_surface.npy'), surf_arr)
     np.save(os.path.join('test_input_data','input_upper.npy'), upper_arr)
     print('Есть 1 сохранение')

     surf_arr_few_day = np.array(surface_data_list_few_day)
     upper_arr_few_day = np.array(upper_data_list_few_day)
     np.save(os.path.join('output_data','output_surface_few_day.npy'), surf_arr_few_day)
     np.save(os.path.join('output_data','output_upper_few_day.npy'), upper_arr_few_day)
     print('Есть 2 сохранение')





     