'''
Файлы должны лежать в 'output_data' - согласно указаниям к иерархии директорий Pangu-Weather
Результат - PNG в директории output_data_figs
'''

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys
import os
import shutil

def upper_visualisation(data):
     lats = np.linspace(90, -90, 721)
     lons = np.linspace(0, 359.75, 1440)
     lon, lat = np.meshgrid(lons, lats)

     variables = ['Z', 'Q', 'T', 'U', 'V']
     pressure_levels = [1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 50]

     output_data_figs_dir = os.path.join('output_data_figs','upper_output_data_figs')
     if not os.path.isdir(output_data_figs_dir):
          os.mkdir(output_data_figs_dir)
     else:
          shutil.rmtree(output_data_figs_dir)
          os.mkdir(output_data_figs_dir)

     for variable in variables:
          for pressure_level in pressure_levels:
               try:
                    variable_index = variables.index(variable)
                    pressure_level_index = pressure_levels.index(pressure_level)
                    selected_data = data[variable_index, pressure_level_index, :, :]

                    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
                    ax.coastlines()

                    im = ax.contourf(lon, lat, selected_data, cmap='viridis', transform=ccrs.PlateCarree())

                    cbar = plt.colorbar(im, ax=ax, orientation='vertical', label=f'Значения {variable} на {pressure_level} hPa')

                    plt.title(f'Визуализация {variable} на уровне давления {pressure_level} hPa')
                    plt.xlabel('Долгота')
                    plt.ylabel('Широта')

                    # plt.show()
                    
                    fig_name = f"{variable}_{pressure_level}.png"
                    plt.savefig(os.path.join(output_data_figs_dir,fig_name))
                    plt.close()
               except Exception as e:
                    print(f"There was an error with {variable} at {pressure_level}, type: {e}")

def surface_visualisation(data):
     lats = np.linspace(90, -90, 721)
     lons = np.linspace(0, 359.75, 1440)

     lon, lat = np.meshgrid(lons, lats)

     variables = ['MSLP', 'U10', 'V10', 'T2M']
     
     output_data_figs_dir = os.path.join('output_data_figs','surface_output_data_figs')
     if not os.path.isdir(os.path.join('output_data_figs',output_data_figs_dir)):
          os.mkdir(output_data_figs_dir)
     else:
          shutil.rmtree(output_data_figs_dir)
          os.mkdir(output_data_figs_dir)

     for variable in variables:
          try:
               variable_index = variables.index(variable)
               selected_data = data[variable_index, :, :]

               fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
               ax.coastlines()

               im = ax.contourf(lon, lat, selected_data, cmap='viridis',transform=ccrs.PlateCarree())

               cbar = plt.colorbar(im, ax=ax, orientation='vertical', label=f'Значения {variable}')

               plt.title(f'Визуализация {variable} на поверхности')
               plt.xlabel('Долгота')
               plt.ylabel('Широта')

               # plt.show()
               
               fig_name = f"{variable}.png"
               plt.savefig(os.path.join(output_data_figs_dir,fig_name))
               plt.close()
          except Exception as e:
               print(f"There was an error with {variable}, type: {e}")


if not os.path.isdir('output_data_figs'):
     os.mkdir('output_data_figs')
else:
     shutil.rmtree('output_data_figs')
     os.mkdir('output_data_figs')

for file in os.listdir('output_data'):
     file_path = os.path.join('output_data',file)
     data = np.load(file_path)
     data_list = data.tolist() # debug
     if 'surface' in file_path:
          surface_visualisation(data)
     else:
          upper_visualisation(data)