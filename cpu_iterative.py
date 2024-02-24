import os
import numpy as np
import onnx
import onnxruntime as ort
from datetime import datetime

def cpu_iterative(day_num, model_path="pangu_weather_24.onnx"):
    print(datetime.now())
    input_data_dir = "test_input_data"
    output_data_dir = "output_data"
    
    model = onnx.load(model_path)

    
    options = ort.SessionOptions()
    options.enable_cpu_mem_arena = False
    options.enable_mem_pattern = False
    options.enable_mem_reuse = False
    
    options.intra_op_num_threads = 10

    
    cuda_provider_options = {
        "arena_extend_strategy": "kSameAsRequested",
    }
    
    ort_session_24 = ort.InferenceSession(model_path,sess_options=options,providers=[("CPUExecutionProvider")],)
    # ort_session_24 = ort.InferenceSession('pangu_weather_1.onnx', sess_options=options, providers=[('CUDAExecutionProvider', cuda_provider_options)])

    input = np.load(os.path.join(input_data_dir, "input_upper.npy")).astype(np.float32)
    print("Прочитано")
    input_surface = np.load(os.path.join(input_data_dir, "input_surface.npy")).astype(np.float32)

    input_24, input_surface_24 = input, input_surface

    # inner_difference = []
    # surface_difference = []
    for i in range(day_num):
        print(f"{datetime.now()} : Идёт день: {i+1}")
        output, output_surface = ort_session_24.run(None, {"input": input_24, "input_surface": input_surface_24})
        input_24, input_surface_24 = output, output_surface

    np.save(os.path.join(output_data_dir, f'output_upper_neuro'), output)
    np.save(os.path.join(output_data_dir, f'output_surface_neuro'), output_surface)

    f"{datetime.now()} : Cохранён {day_num}-дневный прогноз"
    
    return output, output_surface