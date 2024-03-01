import math
import os
import numpy as np

def calculate_rmse(day_num, time_type):
     def calculate_rmse_values(selected_forecast_data, selected_truth_data, target_lat_value=-90.0):
          '''
          RMSE = sqrt(
               sum(
                    (forecast[0:721,0:1440]-truth[0:721,0:1440])^2
                    *cos(phi[0:721])
                    ) / sum(cos(phi[0:721]))/1440)
          '''
          sum_difference_forecast = 0.0
          sum_lat_cos = 0.0
          lat_value = 90

          for lat in range(selected_forecast_data.shape[0]):
               lat_cos = math.cos(math.radians(lat_value))
               if lat_value < target_lat_value:
                    break

               for lon in range(selected_forecast_data.shape[1]):
                    difference_forecast = (selected_forecast_data[lat, lon] - selected_truth_data[lat, lon]) ** 2 * lat_cos
                    sum_difference_forecast += difference_forecast

               sum_lat_cos += lat_cos
               lat_value -= 0.25

          return math.sqrt(sum_difference_forecast / sum_lat_cos / 1440)

     def do_work(forecast_data, truth_data, mode):
          if mode == 'upper':
               variables = ['Z', 'Q', 'T', 'U', 'V']
               levels = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]
               target_variables = ['Z']
               target_levels = [500]
               
               rmse_values = []
               for variable in variables:
                    if variable in target_variables:
                         for level in levels:
                              if level in target_levels:
                                   variable_index = variables.index(variable)
                                   level_index = levels.index(level)
                                   
                                   selected_forecast_data = forecast_data[variable_index, level_index, :, :]
                                   selected_truth_data = truth_data[variable_index, level_index, :, :]
                                   rmse_earth = calculate_rmse_values(selected_forecast_data, selected_truth_data)
                                   rmse_norther_hemisphere = calculate_rmse_values(selected_forecast_data, selected_truth_data, 0.0)
                                   print('счёт')
                                   rmse_values.append({
                                        'variable': variable,
                                        'rmse_earth': rmse_earth,
                                        'rmse_norther_hemisphere': rmse_norther_hemisphere,
                                   })
                                   # rmse_values[variable] = 
               
               return rmse_values
                                   
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
     print(f"RMSE for MSLP for the {day_num}-{time_type} forecast:{rmse_earth} in all Earth, {rmse_norther_hemisphere} for norther hemisphere ")
     
     if time_type == 'hour':
               day_num = day_num*6
     with open('rmse.txt', 'a') as file:
          file.write(f"RMSE for MSLP for the {day_num}-{time_type} forecast:{rmse_earth} in all Earth, {rmse_norther_hemisphere} for norther hemisphere\n")

     upper_path_few_day = os.path.join('output_data', 'output_upper_few_day.npy')
     upper_path = os.path.join('output_data', 'output_upper_neuro.npy')
     upper_few_day = np.load(upper_path_few_day).astype(np.float32)
     upper = np.load(upper_path).astype(np.float32)
     rmse_values = do_work(upper, upper_few_day, 'upper')

     for variable in rmse_values:
          print(f'''
     RMSE for 500 level for the {day_num}-{time_type} forecast:
     for {variable['variable']} variable:
     {variable['rmse_earth']} in all Earth, 
     {variable['rmse_norther_hemisphere']} for norther hemisphere\n
     ''')
          with open('rmse.txt', 'a') as file:
               file.write(f"RMSE for 500 level for the {day_num}-{time_type} forecast: for {variable['variable']} variable:{variable['rmse_earth']} in all Earth, {variable['rmse_norther_hemisphere']} for norther hemisphere\n")


# import matplotlib.pyplot as plt
# '''
# RMSE для MSLP
# '''

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

# plt.plot(days, rmses_earth, label='RMSE (Earth)')
# plt.plot(days, rmses_north, label='RMSE (Northern Hemisphere)')
# plt.xlabel('Дни')
# plt.ylabel('RMSE')
# plt.title('MSLP')
# plt.legend()
# plt.show()

# '''
# Z500
# '''
# days = [1,2,3,4,5,6]
# rmses_earth = [
#      1.1982164488643094,
#      2.099772494362849 ,
#      3.2847798354318396 ,
#      5.28038646818699 ,
#      8.214882785794169 ,
#      11.312788294143855,
# ]
# rmses_north = [
#      1.2376438438509612,
#      2.145206872439343,
#      3.3800938291464138,
#      5.3227798267921065,
#      7.677060317417868,
#      9.820631727297625,
# ]

# plt.plot(days, rmses_earth, label='RMSE (Earth)')
# plt.plot(days, rmses_north, label='RMSE (Northern Hemisphere)')
# plt.xlabel('Дни')
# plt.ylabel('RMSE')
# plt.title('Z500')
# plt.legend()
# plt.show()

# '''
# MSLP (с применением 6-часовых итераций и 1-дневных)
# '''
# days = [1,2,3,4]
# rmses_earth_day_iteration = [
#      1.1982164488643094,
#      2.099772494362849 ,
#      3.2847798354318396 ,
#      5.28038646818699
# ]
# rmses_north_day_iteration = [
#      1.6551827531358165,
#      2.710481067526342,
#      3.7417331582567614,
#      5.901391834602682,
# ]
# rmses_earth_6_hour_iteration = [
#      1.657812620657252,
#      3.0198816319897595,
#      4.326787905975324,
#      7.087686600141968,
# ]
# rmses_north_6_hour_iteration = [
#      1.8471202738304817,
#      3.356954831877965,
#      4.897935998128755,
#      8.321543348687966,
# ]

# plt.plot(days, rmses_earth_day_iteration, label='RMSE Earth (1-day iteration)')
# plt.plot(days, rmses_earth_6_hour_iteration, label='RMSE Earth (6-hours iteration)')
# plt.plot(days, rmses_north_day_iteration, label='RMSE Northern Hemisphere (1-day iteration)')
# plt.plot(days, rmses_north_6_hour_iteration, label='RMSE Northern Hemisphere (6-hours iteration)')
# plt.xlabel('Дни')
# plt.ylabel('RMSE')
# plt.title('MSLP')
# plt.legend()
# plt.show()