from nc2npy import nc2npy
from cpu_iterative import cpu_iterative
from calculate_rmse import calculate_rmse
import numpy as np
import os

day_num = 1

nc2npy(day_num)

output_upper, output_surface = cpu_iterative(day_num)
if not os.path.isdir('archieve_output_data'):
     os.mkdir('archieve_output_data')
np.save(os.path.join('archieve_output_data', f'output_upper{day_num}'), output_upper)
np.save(os.path.join('archieve_output_data', f'output_surface{day_num}'), output_surface)

calculate_rmse(day_num)