import math
import os
import numpy as np

def calculate_rmse(day_num):
     def calculate_rmse_values(selected_forecast_data, selected_truth_data, target_lat_value=-90.0):
          '''
          RMSE = sqrt(sum((forecast[0:721,0:1440]-truth[0:721,0:1440])^2*cos(phi[0:721])) / sum(cos(phi[0:721]))/1440)
          '''
          first_flag = True
          lat_value = 90
          for lat in range(selected_forecast_data.shape[0]):
               if lat_value < target_lat_value:
                    break
               
               for lon in range(selected_forecast_data.shape[1]):
                    difference_forecast = (selected_forecast_data[lat,lon]-selected_truth_data[lat,lon])**2*math.cos(math.radians(lat_value))
                    lat_cos = math.cos(math.radians(lat_value))
                    if first_flag:
                         sum_difference_forecast = difference_forecast
                         sum_lat_cos = lat_cos
                         first_flag = False
                    else:
                         sum_difference_forecast+=difference_forecast
                         sum_lat_cos+=lat_cos
               lat_value-=0.25
               
          return math.sqrt(sum_difference_forecast/sum_lat_cos/1440)

     def do_work(forecast_data, truth_data, mode):
          if mode == 'upper':
               pass
                                   
          elif mode == 'surface':
               variables = ['MSLP', 'U10', 'V10', 'T2M']
               target_variables = ['MSLP']
               
               for variable in variables:
                    if variable in target_variables:
                         variable_index = variables.index(variable)
                         selected_forecast_data = forecast_data[variable_index, :, :]
                         # selected_forecast_data_all_test = selected_forecast_data[:]
                         selected_truth_data = truth_data[variable_index, :, :]
                         rmse_earth = calculate_rmse_values(selected_forecast_data, selected_truth_data)
                         rmse_norther_hemisphere = calculate_rmse_values(selected_forecast_data, selected_truth_data, 0.0)
                         return rmse_earth, rmse_norther_hemisphere

     # day_num = 6

     surface_path_few_day = os.path.join('output_data', 'output_surface_few_day.npy')
     surface_path = os.path.join('output_data', 'output_surface_neuro.npy')
     surface_few_day = np.load(surface_path_few_day).astype(np.float32)
     surface = np.load(surface_path).astype(np.float32)
     rmse_earth, rmse_norther_hemisphere = do_work(surface, surface_few_day, 'surface')   
     print(f"RMSE for MSLP for the {day_num}-day forecast:{rmse_earth} in all Earth, {rmse_norther_hemisphere} for norther hemisphere ")
     with open('rmse.txt', 'a') as file:
          file.write(f"RMSE for MSLP for the {day_num}-day forecast:{rmse_earth} in all Earth, {rmse_norther_hemisphere} for norther hemisphere\n")

     upper_path_few_day = os.path.join('output_data', 'output_upper_few_day.npy')
     upper_path = os.path.join('output_data', 'output_upper_neuro.npy')
     upper_few_day = np.load(upper_path_few_day).astype(np.float32)
     upper = np.load(upper_path).astype(np.float32)



# '''
# '''
# import matplotlib.pyplot as plt

# days = [1,2,3,4,5,6]
# rmses_earth = [
#      1.4900317446961968,
#      2.425056010831151 ,
#      3.495120921052075 ,
#      5.434072635976809 ,
#      8.954299443439611 ,
#      11.580264038555082,
# ]
# rmses_north = [
#      1.6551827531358165,
#      2.710481067526342,
#      3.7417331582567614,
#      5.901391834602682,
#      9.434370036893146,
#      11.796832530391685,
# ]

# plt.plot(days, rmses_earth, label='rmses_earth')
# plt.plot(days, rmses_north, label='rmses_north')
# plt.xlabel('Дни')
# plt.ylabel('RMSE')
# plt.legend()

# plt.show()